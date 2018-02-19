// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include "helpers.h"

/* Example 6: Differentiating functions returning vectors */

namespace example6
{
    vector<double> multiplyGroups(vector<double> x, int n)
    {
        double prod = 1;
        vector<double> result;
        for (int i = 0; i < x.size(); ++i)
        {
            prod *= x[i];                        // Step 1
            if ((i + 1) % n == 0)
            {
                result.push_back(prod);
                prod = 1;
            }
        }
        return result;
    }

    void multiplyGroups_AD(vector<double> d_dresult, vector<double> x, int n, vector<double>& d_dx)
    {
        double prod = 1;
        vector<double> result;
        for (int i = 0; i < x.size(); ++i)
        {
            prod *= x[i];                        // Step 1
            if ((i + 1) % n == 0)
            {
                result.push_back(prod);
                prod = 1;
            }
        }

        // Reverse sweep
        for (int i = 0; i < x.size(); ++i)
        {
            int o = i / n; // Index to output array
            auto dresult_dx = result[o] / x[i];  // Step 1 reverse
            d_dx[i] += d_dresult[o] * dresult_dx;
        }
    }

    double polynomial(vector<double> x)
    {
        double result = 0;
        for (int i = 0; i < x.size(); ++i)
            result += x[i] * (i + 1);            // Step 1
        return result;
    }

    void polynomial_AD(double d_dresult, vector<double> x, vector<double>& d_dx)
    {
        double result = 0;
        for (int i = 0; i < x.size(); ++i)
            result += x[i] * (i + 1);            // Step 1

        // Reverse sweep
        for (int i = 0; i < x.size(); ++i)
        {
            double dresult_dx = (i + 1);
            d_dx[i] += d_dresult * dresult_dx;   // Step 1 reverse
        }
    }

    double f(vector<double> x, int n)
    {
        vector<double> y = multiplyGroups(x, n); // Step 1
        double result = polynomial(y); // Step 2
        return result;
    }

    void f_AD(double d_dresult, vector<double> x, int n, vector<double>& d_dx)
    {
        vector<double> y = multiplyGroups(x, n); // Step 1
        double result = polynomial(y);           // Step 2

        // Reverse sweep
        vector<double> d_dy = create_AD(y);      
        polynomial_AD(d_dresult, y, d_dy);       // Step 2 reverse
        multiplyGroups_AD(d_dy, x, n, d_dx);     // Step 1 reverse
    }

    void example6()
    {
        vector<double> x = { 2, 3, 4, 5, 6, 4, 4, 3 };
        int n = 4;
        double y = f(x, n);                      // Step 1
        cout << "y = " << y << endl;

        // Reverse sweep
        double d_dy = 1;                         // Seed
        vector<double> d_dx = create_AD(x);
        f_AD(d_dy, x, n, d_dx);                  // Step 1 reverse
        cout << "dy_dx = " << ToString(d_dx) << endl;

        // Numerical Checks
        CheckEqual(d_dx, FiniteDifference(std::bind(&f, _1, n), x));
    }
}
