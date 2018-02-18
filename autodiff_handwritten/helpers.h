// Copyright © 2018 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include <assert.h>
#include <stdio.h>
#include <functional>
#include <iostream>
#include <memory>
#include <sstream>
#include <vector>

using namespace std;
using std::placeholders::_1;
using std::placeholders::_2;

double create_AD(double v) 
{ 
    return 0; 
}

vector<double> create_AD(const vector<double>& v)
{ 
    return vector<double>(v.size(), 0);
}

double FiniteDifference(function<double(double)> f, double x)
{
    const double d = 1e-6;
    double f_plus = f(x + d);
    double f_minus = f(x - d);
    return (f_plus - f_minus) / (2 * d);
}

vector<double> FiniteDifference(function<double(vector<double>)> f, vector<double> x)
{
    const double d = 1e-6;
    vector<double> out(x.size(), 0);
    for(int i=0; i<x.size(); ++i)
    { 
        vector<double> xp = x;
        vector<double> xm = x;
        xp[i] += d;
        xm[i] -= d;
        out[i] = (f(xp) - f(xm)) / (2 * d);
    }
    return out;
}

string ToString(vector<double> v)
{
    stringstream ss;
    for (double x : v)
        ss << x << " ";
    return ss.str();
}

void CheckEqual(double actual, double expected)
{
    double diff = abs(actual - expected);
    if (diff >= 3e-6)
    {
        stringstream ss;
        ss << "Numerical mismatch: Actual = " << actual << ", Expected = " << expected << ", Difference = " << diff;
        cout << ss.str();
        throw exception(ss.str().c_str());
    }
}

void CheckEqual(vector<double> actual, vector<double> expected)
{
    if (actual.size() != expected.size())
        throw exception("Actual and expected size differs");
    for (int i = 0; i < actual.size(); ++i)
    {
        double diff = abs(actual[i] - expected[i]);
        if (diff >= 3e-6)
        {
            stringstream ss;
            ss << "Numerical mismatch: Actual = " << actual[i] << ", Expected = " << expected[i] << ", Difference = " << diff << " at position " << i;
            cout << ss.str();
            throw exception(ss.str().c_str());
        }
    }
}
