#include "Util.h"
#include "Data.h"
#include "Model.h"
#include "Analyzer.h"
#include "Test.h"

#include <sstream>
#include <fstream>
#include <cstdio>
#include <cstring>

using namespace std;

int     main(int argc,char **args)
{
    int TEST_METHOD = 0;
    int MAX_ITER = 10;
    int ROLE_NUM = 3;
    int TIME_STEP = 3600;
    int MAX_DELAY_TIME = 24;
    int BURN_IN = 5;
    int SAMPLE_LAG = 5;
    double ALPHA = (ROLE_NUM + 0.0) / 50;
    double BETA_0 = 1;
    double BETA_1 = 1;
    double GAMMA_0 = 1;
    double GAMMA_1 = 1;

    string NETWORK_FILE_DIR = "";
    string DIFFUSION_FILE_DIR = "";
    string NETWORK_CONSTRAINT_FILE_DIR = "";
    string PAGE_RANK_FILE_DIR = "";
    string MODEL_FILE_DIR = "model.txt";

    int cnt = 0;
    for (int i = 1; i + 1 < argc;i ++) 
        if (args[i][0]=='-')
        {
            if (args[i][1] == 'n')
            {
			    NETWORK_FILE_DIR = args[i + 1];
                cnt ++;
            }
            if (args[i][1] == 'd')
            {
                DIFFUSION_FILE_DIR = args[i + 1];
                cnt ++;
            }
            if (args[i][1] == 's')
            {
                NETWORK_CONSTRAINT_FILE_DIR = args[i + 1];
                cnt ++;
            }
            if (args[i][1] == 'p')
            {
                PAGE_RANK_FILE_DIR = args[i + 1];
                cnt ++;
            }
            if (args[i][1] == 'i')
                MAX_ITER = atoi(args[i + 1]);
            if (args[i][1] =='k')
                ROLE_NUM = atoi(args[i + 1]);
            if (args[i][1] == 'h')
            {
                printf( "Input parameters:\n");
                printf( "-n  string  :   network file dir\n");
                printf( "-d  string  :   post file dir\n");
                printf( "-p  string  :   PageRank score file dir\n");
                printf( "-s  string  :   NetworkConstraint socre file dir\n");
                printf( "-i  int     :   number of maximum iterations used for learning algorithm [optional, 10 as default]\n");
                printf( "-k  int     :   number of social roles [optional, 3 as default]\n");
                return 0;
            }
        }
    if (cnt < 4 || PAGE_RANK_FILE_DIR.length() < 1 || NETWORK_CONSTRAINT_FILE_DIR.length() < 1 || DIFFUSION_FILE_DIR.length() < 1 || NETWORK_CONSTRAINT_FILE_DIR.length() < 1)
    {
        printf( "##### Social Role-aware Information Diffusion Model #####");
        printf( "Input parameters:\n");
        printf( "-n  string  :   network file dir\n");
        printf( "-d  string  :   post file dir\n");
        printf( "-p  string  :   PageRank score file dir\n");
        printf( "-s  string  :   NetworkConstraint socre file dir\n");
        printf( "-i  int     :   number of maximum iterations used for learning algorithm [optional, 10 as default]\n");
        printf( "-k  int     :   number of social roles [optional, 3 as default]\n");
        printf("###########################################################\n");
        printf("Error information:\n");
        if (PAGE_RANK_FILE_DIR.length() < 1)
            printf("Missing PageRank score file!\n");
        if (NETWORK_CONSTRAINT_FILE_DIR.length() < 1)
            printf("Missing NetworkConstraint score file!\n");
        if (NETWORK_FILE_DIR.length() < 1)
            printf("Missing network file!\n");
        if (DIFFUSION_FILE_DIR.length() < 1)
            printf("Missing post file!\n");
        return -1;
    }
    
    DataLoader* dataLoader = new DataLoader();
    //Analyzer* analyzer = new Analyzer();

    dataLoader -> TIME_STEP = TIME_STEP;
    dataLoader -> NETWORK_FILE_DIR = NETWORK_FILE_DIR;
    dataLoader -> DIFFUSION_FILE_DIR = DIFFUSION_FILE_DIR;
    dataLoader -> NETWORK_CONSTRAINT_FILE_DIR = NETWORK_CONSTRAINT_FILE_DIR;
    dataLoader -> PAGE_RANK_FILE_DIR = PAGE_RANK_FILE_DIR;
    dataLoader -> LoadData();

    Model* model;
    //printf("#role = %d\n", ROLE_NUM);
    model = new Model();
    //model -> dataLoader = dataLoader;
    model -> LoadData(dataLoader);
    model -> alpha = ALPHA;
    model -> beta_0 = BETA_0;
    model -> beta_1 = BETA_1;
    model -> gamma_0 = GAMMA_0;
    model -> gamma_1 = GAMMA_1;
    model -> roleNum = ROLE_NUM;
    model -> maxTime = MAX_DELAY_TIME;

    Test* test = new Test();
    test -> model = model;
    test -> TrueSize();
    test -> TrueDuration();
    
    if (TEST_METHOD == 0)
    {
        model -> GibbsSampling(MAX_ITER, BURN_IN, SAMPLE_LAG);
        model -> Save(MODEL_FILE_DIR);
    }
    //model -> RoleLevelTest();
    model -> Test();
    
    //test -> SizeAndDuration(TEST_METHOD);
    //test -> DurationTest();
    /*
    analyzer -> nodeList = dataLoader -> nodeList;
    analyzer -> postList = dataLoader -> postList;
    */
    /*
    for (int plan = 0; plan < 3; plan ++)
    {
        printf("Plan: %d\n", plan);
        analyzer -> CalcNetworkConstraint(plan);
    }
    */
    //analyzer -> ActiveNeighbor(1, 1);
    return 0;
}

