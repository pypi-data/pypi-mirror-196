/*************************************************************************
 *
 *  Project
 *                        __  __ _______ _____  _  __
 *                       |  \/  |__   __|  __ \| |/ /
 *  ___  _ __   ___ _ __ | \  / |  | |  | |__) | ' /
 * / _ \| '_ \ / _ \ '_ \| |\/| |  | |  |  ___/|  <
 *| (_) | |_) |  __/ | | | |  | |  | |  | |    | . \
 * \___/| .__/ \___|_| |_|_|  |_|  |_|  |_|    |_|\_\
 *      | |
 *      |_|
 *
 *
 * Copyright (C) Akiel Aries, <akiel@akiel.org>, et al.
 *
 * This software is licensed as described in the file LICENSE, which
 * you should have received as part of this distribution. The terms
 * among other details are referenced in the official documentation
 * seen here : https://akielaries.github.io/openMTPK/ along with
 * important files seen in this project.
 *
 * You may opt to use, copy, modify, merge, publish, distribute
 * and/or sell copies of the Software, and permit persons to whom
 * the Software is furnished to do so, under the terms of the
 * LICENSE file. As this is an Open Source effort, all implementations
 * must be of the same methodology.
 *
 *
 *
 * This software is distributed on an AS IS basis, WITHOUT
 * WARRANTY OF ANY KIND, either express or implied.
 *
 ************************************************************************/

/*
 * stubbed out implementation file for arithmetic operations
 */
#include "../../include/arithmetic.hpp"
#include <cstdint>

int64_t mtpk::Basics::greatest_power(int64_t n, int64_t p) {
    int64_t result = 0;

    // Calculate x = n/p + n/(p^2) + n/(p^3) + ....
    while (n) {
        n /= p;
        result += n;
    }
    return result;
}

int64_t mtpk::Basics::op_gcd(int64_t x, int64_t y) {
    if (x < y)
        return op_gcd(y, x);

    else if (x % y == 0)
        return y;

    else
        return op_gcd(y, x % y);
}
