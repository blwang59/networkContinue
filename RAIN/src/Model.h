#pragma once

#include "Data.h"

#include <algorithm>
#include <string>
#include <vector>
#include <map>
#include <set>

using namespace std;

class       Model	
{
public:
    // parameters
    int                 V;          // number of users
    int                 M;          // number of posts
    int                 S;          // number of sourcee posts
    int                 roleNum;    // number of roles
    int                 K;          // numebr of features
    int                 maxTime;    // maximum delay time
    double              tau0;
    double              tau1;
    double              tau2;
    double              tau3;
    double              alpha;
    double              beta_0;     // hyper-parameter of lambda; success
    double              beta_1;         
    double              gamma_0;    // hyper-parameter of rho; fail
    double              gamma_1;    // hyper-parameter of rho
    double*             rho;        // role-active prob (Bionomial)
    double*             lambda;     // role-delay prob (geometric)
    double**            theta;      // user-role prob (Multinomial)
    double**            mu;         // role-feature mean in Gaussian
    double**            delta;      // role-feature variance in Gaussian
    
    int**               R;
    int**               T;
    int**               Z;
    int**               nur;
    int*                nr;
    int*                nu;
    int**               nrz;
    int**               sumz_v;
    int**               sumt_v;
    int*                sumt_r;
    int**               E;
    int**               nz_t;
    double**            sumz_m;
    double**            sumz_s;
    double*             sum_lambda;
    double*             sum_rho;
    double**            sum_mu;
    double**            sum_delta;

    vector<Node*>       nodeList;
    vector<Post*>       postList;
    map<int, int>       userIdMap;
    DataLoader*         dataLoader;

    int                 Init();
    int                 PrintNr();
    int                 SampleRTZ(int u, int v, int y, int tiu, int tiv, int sumtv, int sumzv);
    int                 SampleDiffusion();
    int                 SampleFeature();
    int                 SampleRole(int u, double x, int t);
    int                 GetOrInsertUserId(int key);
    int                 GetUserId(int key);
    int                 LoadData(DataLoader* dataLoader);
    int                 GibbsSampling(int maxIter, int BURN_IN, int SAMPLE_LAG);
    int                 PrintMu();
    int                 PrintRho();
    int                 PrintTheta();
    int                 Save(string fileDir);
    int                 SaveGaussian();
    int                 SaveRho();
    int                 SaveTheta();
    int                 Test();
    int                 RoleLevelTest();
};
