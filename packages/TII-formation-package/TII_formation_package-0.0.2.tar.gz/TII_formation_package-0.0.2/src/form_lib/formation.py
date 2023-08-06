#! /usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

class Formation:
    def __init__(self, state_sharing, node, form, angle, attr_x, dist_x):
        self.node = node
        self.states = state_sharing
        self.formation = form
        self.attr_x = attr_x
        self.dist_x = dist_x
        self.PLANE_ANGLE = angle * np.pi/180

    def get_control(self):
        dist_x = np.array([0.0, 0.0, 0.0])
        form = np.array([0.0, 0.0, 0.0])
        disty_left = []
        disty_right = []
        d_signed = []

        # direction of flight
        direction = np.array(
            [np.cos(self.PLANE_ANGLE - np.pi/2),
             np.sin(self.PLANE_ANGLE - np.pi/2), 0])

        own_position = np.array([
            self.states.me.lat, self.states.me.lon, self.states.me.alt
        ])

        swarming_agents = [a for a in self.states.agents.values()
                           if a.ident not in self.landing_agents and 'm' not in a.ident]
        for agent in swarming_agents:
            # relative position:
            agent_position = np.array([agent.lat, agent.lon, agent.alt])

            dp_global = convert_position_to_local(
                own_position, agent_position
            )

            dp_x = self.project(dp_global, self.PLANE_ANGLE - np.pi/2)
            dp_y = self.project(dp_global, self.PLANE_ANGLE)

            dp_x[2] = 0
            dp_y[2] = 0

            if self.formation == 'line':
                attr_x = self.attr_x*dp_x
                dist_x += attr_x

            d_signed.append(np.dot(dp_x, direction))

            # angle between the drones
            theta = np.arctan2(dp_y[1],dp_y[0])

            if np.cos(theta) > 0:
                disty_left.append(dp_y[1])
            else:
                disty_right.append(dp_y[1])

        # number of drones on each side
        n_left = len(disty_left)
        n_right = len(disty_right)

        # adding drones own distance
        d_signed.append(0)

        if self.dist_x != 0:
            match self.formation:
                case 'arrow':
                    if (len(swarming_agents) + 1) % 2 == 0:
                        A1 = (((len(swarming_agents) + 1)//2) -
                             abs(n_left-n_right))
                    else:
                        A1 = ((len(swarming_agents) + 1)//2)/2 + \
                            (((len(swarming_agents) + 1)//2) -
                             max(n_left, n_right))
                case 'vee':
                    if (len(swarming_agents) + 1) % 2 == 0:
                        A1 = -(((len(swarming_agents) + 1)//2) -
                             abs(n_left-n_right))
                    else:
                        A1 = -((len(swarming_agents) + 1)//2)/2 - \
                            (((len(swarming_agents) + 1)//2) -
                             max(n_left, n_right))
                case 'r_diagonal':
                    A1 = (- n_right + n_left)/2
                case 'l_diagonal':
                    A1 = (n_right - n_left)/2
                case 'line':
                    form, A1 = 0, 0
            if self.formation != 'line':
                form = (np.mean([np.min(d_signed), np.max(d_signed)]) +
                        A1 * self.dist_x) * direction
                
        return form, dist_x


def gps_coord_to_dist(lat1, lon1, lat2, lon2):
    lat1_rad = lat1 * np.pi / 180
    lat2_rad = lat2 * np.pi / 180
    lon1_rad = lon1 * np.pi / 180
    lon2_rad = lon2 * np.pi / 180
    R = 6378137  # Radius of earth in m
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = (
        np.sin(dlat/2)**2 +
        np.cos(lat1_rad) * np.cos(lat2_rad) * np.sin(dlon/2)**2
    )
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1-a))
    d = R * c
    return d


def lat_dist(lat1, lat2):
    dist = gps_coord_to_dist(lat1, 0, lat2, 0)
    if lat1 < lat2:
        return dist
    else:
        return -dist


def lon_dist(lon1, lon2, lat):
    dist = gps_coord_to_dist(lat, lon1, lat, lon2)
    if lon1 < lon2:
        return dist
    else:
        return -dist


def convert_position_to_local(own_position, other_position):
    x = lat_dist(own_position[0], other_position[0])
    y = lon_dist(own_position[1], other_position[1], own_position[0])
    return np.array([x, y, other_position[2] - own_position[2]])


def project(self, dp, angle=0):
    xy_vector = dp[:2]
    proj_vector = np.array([np.cos(angle), np.sin(angle)])

    result = (
    xy_vector.dot(proj_vector) /
    proj_vector.dot(proj_vector)*proj_vector
    )
    return np.array([result[0], result[1], dp[2]])
