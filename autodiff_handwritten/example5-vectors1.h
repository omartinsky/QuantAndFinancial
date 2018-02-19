// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include "helpers.h"

/* Example 5: Differentiating function with vector arguments */

namespace example5
{
    double f(vector<double> x)
    {
        double mult = 1;
        for (int i = 0; i < x.size(); ++i)
            mult *= (1 + x[i]);                  // Step 1
        double result = mult - 1;
        return result;
    }

    void f_AD(double d_dresult, vector<double> x, vector<double>& d_dx)
    {
        double mult = 1;
        for (int i = 0; i < x.size(); ++i)
            mult *= (1 + x[i]);                  // Step 1
        
        // Reverse sweep
        for (int i = 0; i < x.size(); ++i)
            d_dx[i] += mult / (1 + x[i]);        // Step 1 reverse
    }

    void example5()
    {
        vector<double> x = { .01, .03, .02 };
        double y = f(x);                         // Step 1
        cout << "y = " << y << endl;
        
        // Reverse sweep
        double d_dy = 1;                         // Seed
        vector<double> d_dx = create_AD(x);
        f_AD(d_dy, x, d_dx);                     // Step 1 reverse
        cout << "dy_dx = " << ToString(d_dx) << endl;

        // Numerical Checks
        CheckEqual(d_dx, FiniteDifference(std::bind(&f, _1), x));
    }
}
