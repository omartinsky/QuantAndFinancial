// Copyright © 2016 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#include <functional>
#include <math.h>
#include <iomanip>
#include <algorithm>
#include <assert.h>
#include <sstream>
#include "ad_engine.hpp"

#include "unit_tests.hpp"

using namespace std;

double numerical_derivative(function<double(double)> f, double x)
{
    double d = 1e-6;
    return (f(x + d) - f(x - d)) / (2 * d);
}

double numerical_derivative(function<double(double, double)> f, double x, double y, int which)
{
    double d = 1e-6;
    if (which==0)
        return (f(x + d, y) - f(x - d, y)) / (2 * d);
    else
        return (f(x, y + d) - f(x, y - d)) / (2 * d);
}

#define CHECK(actual, expected)     check((actual), (expected), __LINE__)

void check(double actual, double expected, int line)
{
    double absdiff = abs(actual - expected);
    double reldiff = absdiff / max(abs(actual), abs(expected));

    if (reldiff > 1e-6 && absdiff > 1e-10)
    {
        stringstream ss;
        ss << "Error Line=" << line;
        ss << ", Actual=" << setw(10) << actual << endl;
        ss << ", Expected=" << setw(10) << expected << endl;
        ss << ", AbsDiff=" << setw(10) << absdiff << endl;
        ss << ", RelDiff=" << setw(10) << reldiff << endl;
        throw exception(ss.str().c_str());
    }

}

void unit_tests()
{
    {
        ADEngine e;
        ADDouble a(e, 3.);

        auto f = [&](auto x) -> auto {
            return ADDouble(e, 1.0);
        };
        CHECK(e.get_derivative(f(a), a), 0.0);
    }

    {
        ADEngine e;
        ADDouble a(e, 3.);

        auto f = [](auto x) -> auto {
            return x;
        };
        CHECK(e.get_derivative(f(a), a), 1.0);
    }

    {
        ADEngine e;
        ADDouble a(e, 3.);

        auto f = [](auto x) -> auto {
            return x + x + x + x;
        };
        CHECK(e.get_derivative(f(a), a), numerical_derivative(f, a.get_value()));
    }

    {
        ADEngine e;
        ADDouble a(e, 3.);

        auto f = [](auto x) -> auto {
            return (x + x) + (x + x);
        };
        CHECK( e.get_derivative(f(a), a), numerical_derivative(f, a.get_value()));
    }

    {
        ADEngine e;
        ADDouble a(e, 3.);
        ADDouble b(e, 4.);

        auto f = [](auto x, auto y) -> auto {
            return log(x) + log(x) + exp(y) + (x + y) * (2. * x - y) / (x - 0.5 * y) / y;
        };
        CHECK(e.get_derivative(f(a, b), a), numerical_derivative(f, a.get_value(), b.get_value(), 0));
    }
}