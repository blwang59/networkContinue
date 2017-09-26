#pragma once

#include "Data.h"
#include "Model.h"

#include <algorithm>
#include <string>
#include <vector>
#include <map>
#include <set>

using namespace std;

class           Test	
{
public:
    Model*              model;
    int*                diffusionSize;
    int*                diffusionDuration;

    int                 Simulation(int method);
    int                 SampleRole(int u);
    int                 SampleT(int r);
    int                 SampleT(Node* user);
    int                 SampleZ(int r);
    int                 SampleZ(Node* user);
    int                 TrueSize();
    int                 TrueDuration();
    int                 SizeAndDuration(int method);
};
