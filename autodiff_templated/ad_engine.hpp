// Copyright © 2016 Ondrej Martinsky, All rights reserved
// www.quantandfinancial.com

#pragma once

#include <iostream>
#include <string>
#include <vector>
#include <map>
#include <set>

#define AD_ENABLE_LOGGING

using namespace std;

typedef int NodeId; // Variables represent nodes in the derivative tree

class ADEngine;

class ADDouble
{
public:
    ADDouble(ADEngine& engine, double value);
    double get_value() const { return _value; }

    double _value;
    ADEngine& _engine;
    NodeId _id;
};

class ADEngine
{
public:
    typedef map<NodeId, map<NodeId, double>> DerivativeTable; // [Dependent, Independent] -> Value

    ADEngine() : _id_counter(0) {}
    void add_direct_derivative(const ADDouble& of, const ADDouble& wrt, double value);
    double get_derivative(const ADDouble& of, const ADDouble& wrt);

private:
    double get_derivative(NodeId dependent, NodeId independent);

    map<NodeId, ADDouble> _variables;
    DerivativeTable _derivatives;
    set<NodeId> _independent_variables;
    NodeId _id_counter;

    friend class ADDouble;
};

namespace logging
{
    inline string getVariableName(const ADDouble& var)
    {
        return "AD" + std::to_string(var._id);
    }

    inline string getVariableName(const double&)
    {
        return "CONST";
    }

    inline double getValue(const ADDouble& var)
    {
        return var.get_value();
    }

    inline double getValue(const double& var)
    {
        return var;
    }

    template <typename TL, typename TR>
    void logBinaryOperation(string op, const ADDouble& result, const TL& l, const TR& r)
    {
        cout << "Operation "
            << getVariableName(result) << " := "
            << getVariableName(l) << " " << op << " "
            << getVariableName(r) << " = "
            << getValue(l) << " " << op << " " << getValue(r)  << endl;
    }

    inline void logUnaryOperation(string op, const ADDouble& result, const ADDouble& x)
    {
        cout << "Operation "
            << getVariableName(result) << " := " << op + "(" << getVariableName(x) << ") = "
            << op << "(" << getValue(x) << ")" << endl;
    }
}

inline ADDouble operator+(const ADDouble& l, const ADDouble& r)
{
    ADEngine& e = l._engine;
    ADDouble out(e, l._value + r._value);
#ifdef AD_ENABLE_LOGGING
    logging::logBinaryOperation("+", out, l, r);
#endif
    e.add_direct_derivative(out, l, 1.);
    e.add_direct_derivative(out, r, 1.);
    return out;
}

inline ADDouble operator-(const ADDouble& l, const ADDouble& r)
{
    ADEngine& e = l._engine;
    ADDouble out(e, l._value - r._value);
#ifdef AD_ENABLE_LOGGING
    logging::logBinaryOperation("-", out, l, r);
#endif
    e.add_direct_derivative(out, l, 1.);
    e.add_direct_derivative(out, r, -1.);
    return out;
}

inline ADDouble operator*(const ADDouble& l, const ADDouble& r)
{
    ADDouble out(l._engine, l._value * r._value);
#ifdef AD_ENABLE_LOGGING
    logging::logBinaryOperation("*", out, l, r);
#endif
    ADEngine& e = out._engine;
    e.add_direct_derivative(out, l, r._value);
    e.add_direct_derivative(out, r, l._value);
    return out;
}

inline ADDouble operator*(double l, const ADDouble& r)
{
    ADDouble out(r._engine, l * r._value);
#ifdef AD_ENABLE_LOGGING
    logging::logBinaryOperation("*", out, l, r);
#endif
    ADEngine& e = out._engine;
    e.add_direct_derivative(out, r, l);
    return out;
}

inline ADDouble operator/(const ADDouble& l, const ADDouble& r)
{
    ADDouble out(l._engine, l._value * r._value);
#ifdef AD_ENABLE_LOGGING
    logging::logBinaryOperation("/", out, l, r);
#endif
    ADEngine& e = out._engine;
    e.add_direct_derivative(out, l, 1.0 / r._value);
    e.add_direct_derivative(out, r, -l._value / r._value);
    return out;
}

inline ADDouble exp(const ADDouble& x)
{
    double ex = exp(x._value);
    ADDouble out(x._engine, ex);
#ifdef AD_ENABLE_LOGGING
    logging::logUnaryOperation("exp", out, x);
#endif
    ADEngine& e = out._engine;
    e.add_direct_derivative(out, x, ex);
    return out;
}

inline ADDouble log(const ADDouble& x)
{
    ADDouble out(x._engine, log(x._value));
#ifdef AD_ENABLE_LOGGING
    logging::logUnaryOperation("log", out, x);
#endif
    ADEngine& e = out._engine;
    e.add_direct_derivative(out, x, 1/x._value);
    return out;
}
