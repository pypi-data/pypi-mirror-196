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

#include "k-NN.h"
#include <algorithm>
#include <fstream>
#include <iostream>
#include <string>
#include <vector>

using namespace std;

/*
 * For this particular exmaple this is a class which contains the
 * turnover and success of a company and the characteristics of the
 * team. The file with the data will be a csv file whit 3 columns:
 *   - turover(int)
 *   - characteristics(unsigned)
 *   - success(boolean)
 */
class Company {
    public:
    Company(int64_t turnover, string characteristics, bool success)
        : turnover(turnover), success(success), distance(-1) {
        this->characteristics = transformCharacteristics(characteristics);
    }

    // distance from test point
    double distance;
    int64_t turnover;
    int64_t characteristics;
    bool success;

    private:
    /*
     * Function that transforms characteristics (Very
     * Strong,Strong,Average,Weak) as strings to number. It is geting
     * the ASCII code as decimal number and retuning the total sum of
     * all characters within the string.
     */
    int64_t transformCharacteristics(string &c) {
        uint64_t sum = 0;
        for (size_t i = 0; i < c.size(); ++i) {
            if (c[i] != ' ') {
                sum += (int64_t)c[i];
            }
        }
        return sum;
    }
};

/*
 * A class that represent the reader of files with csv extensions.
 */
class CSVReader {
    public:
    CSVReader(const string &fileName, const string &delimeter = ",")
        : fileName(fileName), delimeter(delimeter) {
    }

    /*
     * Function to fetch the data from a CSV file
     */
    vector<vector<string>> getData() {
        ifstream file(this->fileName);
        vector<vector<string>> data;
        string line = "";

        while (getline(file, line)) {
            vector<string> tmp;
            tmp = this->split(line, ",");
            data.push_back(tmp);
        }
        file.close();
        return data;
    }

    private:
    string fileName;
    string delimeter;

    /*
     * Function used to split each line by the delim
     */
    vector<string> split(string target, string delim) {
        vector<string> v;
        if (!target.empty()) {
            size_t start = 0;
            do {
                size_t x = target.find(delim, start);
                // a check whether the target is found
                if (x == -1) {
                    break;
                }
                string tmp = target.substr(start, x - start);
                v.push_back(tmp);
                start += delim.size() + tmp.size();
            } while (true);

            v.push_back(target.substr(start));
        }
        return v;
    }
};

// function used to compare two companies when sorting
bool comparison(Company &lhs, Company &rhs) {
    return lhs.distance < rhs.distance;
}

long double euclideanDistance(Company &lhs, Company &test) {
    return sqrt(pow((lhs.turnover - test.turnover), 2) +
                pow((lhs.characteristics - test.characteristics), 2));
}

long double manhattanDistance(Company &lhs, Company &test) {
    return (abs(lhs.turnover - test.turnover) +
            abs(lhs.characteristics - test.characteristics));
}

void fillDistances(vector<Company> &data, Company &test,
                   double (*distanceFunction)(Company &, Company &)) {
    for (size_t i = 0; i < data.size(); ++i) {
        data[i].distance = distanceFunction(data[i], test);
    }
}

bool KNN(vector<Company> &data, Company &test, int k,
         double (*distanceFunction)(Company &, Company &)) {
    // filling the distances between all points and test
    fillDistances(data, test, distanceFunction);

    // sorting so that we can get the k nearest
    sort(data.begin(), data.end(), comparison);

    int64_t countSuccesful = 0;
    int64_t countUnsuccesful = 0;
    for (int64_t i = 0; i < k; ++i) {
        if (data[i].success) {
            ++countSuccesful;
        } else {
            ++countUnsuccesful;
        }
    }
    /*
     * Based on the count of succesful and unsuccessful examples
     * within those k, we are deciding whether the test example is
     * successful or not.
     */
    if (countSuccesful == countUnsuccesful) {
        test.success = data[0].success;
    } else {
        test.success = countSuccesful > countUnsuccesful ? true : false;
    }
    return test.success;
}

int main() {
    const string path = "../data/zip.test.gz";
    CSVReader reader(path);
    vector<vector<string>> rawData = reader.getData();
    vector<Company> data;
    for (vector<string> line : rawData) {
        Company comp(stoi(line[0]), line[1],
                     line[2] == "1" ? true : false);
        data.push_back(comp);
    }

    /* Test examples
     * 1256 Weak - should return Successful
     * 725 Weak - should return Unsuccessful
     * 1471 Average - should return Successful
     * 703 Very Strong - should return Unsuccessful
     * 1301 Strong - should return Successful
     */
    Company test(703, "Very Strong", true);

    string answer = KNN(data, test, 12, euclideanDistance)
                        ? "Successful"
                        : "Unsuccessful";
    cout << answer;
}
