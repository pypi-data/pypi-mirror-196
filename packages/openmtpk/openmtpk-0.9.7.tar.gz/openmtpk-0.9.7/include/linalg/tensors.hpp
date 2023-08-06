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

/**
 * @ file
 *
 * Definitions for methods involed in creating Tensors
 *
 */

#ifndef TENSORS_HPP
#define TENSORS_HPP

#include <cmath>
#include <vector>

namespace mtpk {

/**
 * @class Vectors
 * @brief Operations related to Vectors and Scalars
 */
class Tensors {
    public:
    std::vector<std::vector<double>>
        tensor_vec_mult(std::vector<std::vector<std::vector<double>>> A,
                        std::vector<double> b);

    void printTensor(std::vector<std::vector<std::vector<double>>> A);
    std::vector<std::vector<std::vector<double>>>
        vector_wise_tensor_product(
            std::vector<std::vector<std::vector<double>>> A,
            std::vector<std::vector<double>> B);
};

} // namespace mtpk

#endif
