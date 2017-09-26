#include "Util.h"
#include "Model.h"
#include "Data.h"

#include <algorithm>
#include <sstream>
#include <fstream>
#include <cstdio>
#include <cstring>
#include <string>
#include <vector>
#include <set>
#include <map>
#include <complex>
#include <utility>
#include <fstream>
#include <iostream>
#include <dirent.h>
#include <unistd.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <cmath>

#define PI          3.141592653
#define EE          2.718281828459
#define MAXINT      10000000

using namespace std;

int             Model::LoadData(DataLoader* dataLoader)
{
    postList = dataLoader -> postList;
    nodeList = dataLoader -> nodeList;
    V = (int) nodeList.size();
    M = (int) postList.size();
    S = (int) dataLoader -> sourceIdMap.size();
    K = (int) dataLoader -> nodeList[0] -> featureList.size();
    printf("#source posts: %d, #users: %d, #posts: %d\n", S, V, M);
    return 0;
}

double          Random()
{
    return 1.0 * rand() / RAND_MAX;
}

int             Model::Init()
{
    rho = new double[roleNum];
    lambda = new double[roleNum];
    mu = new double*[roleNum];
    delta = new double*[roleNum];
    theta = new double*[V];
    R = new int*[M];
    T = new int*[M];
    Z = new int*[M];
    nur = new int*[V];
    nr = new int[roleNum];
    nu = new int[V];
    sumz_v = new int*[S];
    sumt_v = new int*[S];
    E = new int*[V];
    nz_t = new int*[roleNum];
    nrz = new int*[roleNum];
    sumt_r = new int[roleNum];
    sumz_m = new double*[roleNum];
    sumz_s = new double*[roleNum];

    int instanceNum = V * K;
    tau1 = instanceNum;
    tau2 = (instanceNum + 0.0) / 2.0;
    tau3 = 0.0;
    tau0 = 0.0;
    for (int v = 0; v < V; v ++)
    {
        for (int t = 0; t < K; t ++)
        {
            tau0 += nodeList[v] -> featureList[t];
        }
    }
    tau0 /= instanceNum;
    for (int v = 0; v < V; v ++)
    {
        for (int t = 0; t < K; t ++)
        {
            tau3 += pow((nodeList[v] -> featureList[t] - tau0), 2);
        }
    }
    tau3 /= 2;
    for (int v = 0; v < V; v ++)
    {
        nu[v] = 0;
        theta[v] = new double[roleNum];
        nur[v] = new int[roleNum];
        E[v] = new int[K];
        for (int r = 0; r < roleNum; r ++)
        {
            theta[v][r] = 0.0;
            nur[v][r] = 0;
        }
    }
    for (int r = 0; r < roleNum; r ++)
    {
        mu[r] = new double[K];
        delta[r] = new double[K];
        nz_t[r] = new int[K];
        nrz[r] = new int[2];
        sumz_m[r] = new double[K];
        sumz_s[r] = new double[K];
        nrz[r][0] = 0;
        nrz[r][1] = 0;
        sumt_r[r] = 0;
        nr[r] = 0.0;
        for (int t = 0; t < K; t ++)
        {
            nz_t[r][t] = 0;
            mu[r][t] = 0.0;
            delta[r][t] = 0.0;
            sumz_m[r][t] = 0.0;
            sumz_s[r][t] = 0.0;
        }
    }
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Node* user = postList[i] -> user;
        int l = (int) user -> inEdgeList.size(); 
        R[i] = new int[l];
        T[i] = new int[l];
        Z[i] = new int[l];
    }
    for (int s = 0; s < S; s ++)
    {
        sumz_v[s] = new int[V];
        sumt_v[s] = new int[V];
        for (int v = 0; v < V; v ++)
        {
            sumz_v[s][v] = 0;
            sumt_v[s][v] = 0;
        }
    }
    
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        Node* source = post -> user;
        int u = source -> id;
        int sid = post -> sourceId;
        int tiu = post -> postTime;
        for (unsigned int j = 0; j < source -> inEdgeList.size(); j ++)
        {
            Node* target = source -> inEdgeList[j];
            int pid = target -> GetPostIdBySource(post -> sourcePost -> id);
            int tiv = MAXINT;
            if (pid != -1)
                tiv = postList[pid] -> postTime;
            if (pid != -1 && tiv < tiu)
                continue;
            int v = target -> id;
            // sampling
            int y = 1;
            if (pid == -1)
                y = 0;
            int r = (int) (Random() * roleNum);
            if (r == roleNum)
                r --;
            int t = (int) (Random() * maxTime);
            if (t == maxTime)
                t --;
            int z = (int) (Random() * 2);
            if (z == 2)
                z --;
            if (y == 1 && sumt_v[sid][v] == 0)
            {
                t = tiv - tiu;
            }
            if (y == 1 && sumz_v[sid][v] == 0)
                z = 1;
            //if (i == 0 && j < 2)
            //    printf("%d %d %d %d\n", tiv, tiu, t, r);
            // update
            int tv = 0;
            if (t + tiu == tiv)
                tv = 1;
            if (t >= maxTime)
                t = maxTime - 1;
            R[i][j] = r;
            T[i][j] = t;
            Z[i][j] = z;
            nur[u][r] ++;
            nu[u] ++;
            nr[r] ++;
            nrz[r][z] ++;
            sumt_r[r] += t;
            sumz_v[sid][v] += z;
            sumt_v[sid][v] += tv;
        }
    }
    for (int v = 0; v < V; v ++)
    {
        Node* user = nodeList[v];
        for (int t = 0; t < K; t ++)
        {
            double x = user -> featureList[t];
            int r = (int) (Random() * roleNum);
            if (r == roleNum)
                r --;
            E[v][t] = r;
            nur[v][r] ++;
            nu[v] ++;
            nz_t[r][t] ++;
            sumz_m[r][t] += x;
        }
    }
    for (int r = 0; r < roleNum; r ++)
    {
        for (int t = 0; t < K; t ++)
        {
            sumz_m[r][t] /= nz_t[r][t];
        }
    }
    for (int v = 0; v < V; v ++)
    {
        for (int t = 0; t < K; t ++)
        {
            int r = E[v][t];
            int x = nodeList[v] -> featureList[t];
            sumz_s[r][t] += pow((x - sumz_m[r][t]), 2);
        }
    }
    for (int r = 0; r < roleNum; r ++)
    {
        for (int t = 0; t < K; t ++)
            sumz_s[r][t] /= nz_t[r][t];
    }
    return 0;
}

double          Gaussian(double x, double u, double d)
{
    d += 1e-1;
    static const float inv_sqrt_2pi = 0.3989422804014327;
    double a = (x - u) / d;
    double res = inv_sqrt_2pi / d * exp(-0.5f * a * a);
    return res / 1e10;
}

double          GammaFunction(double x)
{
    double res = 0.5 * (log(2 * PI) - log(x)) + x * (log(x + 1 / (12.0 * x - 1.0 / (10 * x))) - 1);
    return res;
    //return pow(EE, res);
}

int                     Model::SampleRole(int u, double x, int t)
{
    double RAlpha = roleNum * alpha;
    double* p = new double[roleNum];
    for (int r = 0; r < roleNum; r ++)
    {
        double tmp_var = nz_t[r][t] * sumz_s[r][t] + x * x + nz_t[r][t] * sumz_m[r][t] * sumz_m[r][t];
        double tmp_mean = (sumz_m[r][t] * nz_t[r][t] + x) / (nz_t[r][t] + 1);
        int tmp_nzt = nz_t[r][t] + 1;
        tmp_var = (tmp_var - tmp_nzt * tmp_mean * tmp_mean) / (tmp_nzt + 0.0);

        double term1 = (nur[u][r] + alpha) / (nu[u] + RAlpha);
        double term2 = GammaFunction(alpha + (tmp_nzt + 0.0) / 2.0) - GammaFunction(alpha + (nz_t[r][t] + 0.0) / 2);
        term2 = pow(EE, term2);
        double tmp_term3 = tau3 + 0.5 * (nz_t[r][t] * sumz_s[r][t] + (tau1 * nz_t[r][t] * pow((sumz_m[r][t] - tau0), 2)) / (tau1 + nz_t[r][t]));
        tmp_term3 = log(tmp_term3) * (tau2 + 0.5 * nz_t[r][t]);
        double term3 = tau3 + 0.5 * (tmp_nzt * tmp_var + (tau1 * tmp_nzt * pow(tmp_mean - tau0, 2)) / (tau1 + tmp_nzt));
        term3 = log(term3) * (tau2 + 0.5 * tmp_nzt);
        term3 = tmp_term3 - term3;
        term3 = pow(EE, term3);
        term3 *= sqrt(tau1 + nz_t[r][t]) / sqrt(tau1 + tmp_nzt);
        //printf("%.3lf %.3lf %.10lf\n", term1, term2, term3);
        p[r] = term1 * term2 * term3;
    }
    // cumulate multinomial parameters
    for (int k = 1; k < roleNum; k ++) 
	    p[k] += p[k - 1];
    // scaled sample because of unnormalized p[]
    double s = ((double) random() / RAND_MAX) * p[roleNum - 1];

    int role = roleNum - 1;
    for (role = 0; role < roleNum - 1; role ++)
	    if (p[role] > s)
	        break;
    //printf("%.3lf %.3lf %d\n", p[K - 1], u, topic);
    delete[] p;
    return role;
}

int                     Model::SampleRTZ(int u, int v, int y, int tiu, int tiv, int sumtv, int sumzv)
{
    double RAlpha = roleNum * alpha;
    double* p = new double[2 * roleNum * maxTime];
    for (int r = 0; r < roleNum; r ++)
    {
        double term1 = (nur[u][r] + alpha + 0.0) / (nu[u] + RAlpha);
        for (int t = 0; t < maxTime; t ++)
        {
            double prod = 1.0;
            for (int tt = 0; tt <= t - 1; tt ++)
            {
                prod *= sumt_r[r] - nr[r] + beta_1 + tt;
            }
            double term2 = (nr[r] + beta_0) * prod;
            prod = 1.0;
            for (int tt = 0; tt <= t; tt ++)
            {
                prod *= (beta_0 + sumt_r[r] + beta_1 + tt);
            }
            term2 /= prod;
            //double term2 = lambda[r] * pow((1 - lambda[r]), t);
            for (int z = 0; z < 2; z ++)
            {
                double term3 = nrz[r][z];
                if (z == 0)
                    term3 += gamma_0;
                else
                    term3 += gamma_1;
                term3 /= (nr[r] + gamma_0 + gamma_1);
                double term4 = 1.0;
                if (y == 0 && z == 1)
                    term4 = 0.0;
                if (y == 1 && sumzv == 0 && z == 0)
                    term4 = 0.0;
                int tv = 0;
                if (t + tiu == tiv)
                    tv = 1;
                if (y == 1 && sumtv == 0)
                {
                    if (tv == 0 && (tiv - tiu < maxTime || t != maxTime - 1))
                        term4 = 0.0;
                    else
                        term4 = 1.0;
                }
                int idx = r * maxTime * 2 + t * 2 + z;
                //printf("%d %d %d : %d\n", r, t, z, idx);
                p[idx] = term1 * term2 * term3 * term4;
                /*
                if (u == 6 && v == 5 && p[idx] > 0)
                {
                    printf("%d %d %d %d %d: %.5lf %.5lf %.5lf %.5lf %.5lf\n", r, t, z, idx, sumzv, term1, term2, term3, term4, p[idx]);
                }
                */
            }
        }
    }
    // cumulate multinomial parameters
    for (int k = 1; k < 2 * roleNum * maxTime; k++) 
	    p[k] += p[k - 1];

    // scaled sample because of unnormalized p[]
    double s = ((double) random() / RAND_MAX) * p[2 * roleNum * maxTime - 1];

    int sample = 2 * roleNum * maxTime - 1;
    for (sample = 0; sample < 2 * roleNum * maxTime - 1; sample ++)
	    if (p[sample] > s)
	        break;
    //printf("%.3lf %.3lf %d\n", p[K - 1], u, topic);
    delete[] p;
    return sample;
}

int             Model::SampleDiffusion()
{
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        Node* source = post -> user;
        int u = source -> id;
        int sid = post -> sourceId;
        int tiu = post -> postTime;
        for (unsigned int j = 0; j < source -> inEdgeList.size(); j ++)
        {
            //printf("%d ", j);
            Node* target = source -> inEdgeList[j];
            //printf("%d\n", target -> id);
            int pid = target -> GetPostIdBySource(post -> sourcePost -> id);
            int tiv = MAXINT;
            if (pid != -1)
                tiv = postList[pid] -> postTime;
            if (pid != -1 && tiv < tiu)
                continue;
            //if (pid != -1 && tiv - tiu - 1 >= maxTime)
            //    printf("Time Exceeds!\n");
            int v = target -> id;
            int old_r = R[i][j];
            int old_t = T[i][j];
            int old_z = Z[i][j];
            int old_tv = 0;
            //printf("old sample: %d %d %d\n", old_r, old_t, old_z);
            if (old_t + tiu == tiv || (tiv - tiu >= maxTime && old_t == maxTime - 1))
                old_tv = 1;
            nur[u][old_r] --;
            nr[old_r] --;
            nu[u] --;
            sumz_v[sid][v] -= old_z;
            sumt_v[sid][v] -= old_tv;
            sumt_r[old_r] -= old_t - 1;
            nrz[old_r][old_z] --;
            //if (sumt_v[sid][v] < 0 && u == 6 && v == 162)
            //    printf("%d %d\n", old_tv);
            // sampling
            int y = 1;
            if (pid == -1)
                y = 0;
            int sample = SampleRTZ(u, v, y, tiu, tiv, sumt_v[sid][v], sumz_v[sid][v]);
            int r = sample / (maxTime * 2);
            int t = (sample % (maxTime * 2)) / 2;
            int z = sample % 2;
            //printf("%d %d %d\n", r, t, z);
            // update
            int tv = 0;
            if (t + tiu == tiv || (tiv - tiu >= maxTime && t == maxTime - 1))
                tv = 1;
            R[i][j] = r;
            T[i][j] = t;
            Z[i][j] = z;
            nur[u][r] ++;
            nu[u] ++;
            nr[r] ++;
            nrz[r][z] ++;
            sumt_r[r] += t + 1;
            sumz_v[sid][v] += z;
            sumt_v[sid][v] += tv;
        }
    }
    return 0;
}

int             Model::SampleFeature()
{
    for (unsigned int i = 0; i < nodeList.size(); i ++)
    {
        Node* user = nodeList[i];
        int u = user -> id;
        for (int t = 0; t < K; t ++)
        {
            double x = user -> featureList[t];
            int old_e = E[u][t];
            nur[u][old_e] --;
            nu[u] --;
            sumz_s[old_e][t] = sumz_s[old_e][t] * nz_t[old_e][t] - x * x + nz_t[old_e][t] * sumz_m[old_e][t] * sumz_m[old_e][t];
            sumz_m[old_e][t] = (sumz_m[old_e][t] * nz_t[old_e][t] - x + 0.0) / (nz_t[old_e][t] - 1);
            nz_t[old_e][t] --;
            sumz_s[old_e][t] = (sumz_s[old_e][t] - nz_t[old_e][t] * sumz_m[old_e][t] * sumz_m[old_e][t]) / (nz_t[old_e][t]);
            int e = SampleRole(u, x, t);

            //printf("%d %d %d\n", i, t, e);
            E[u][t] = e;
            nur[u][e] ++;
            nu[u] ++;
            sumz_s[e][t] = nz_t[e][t] * sumz_s[e][t] + x * x + nz_t[e][t] * sumz_m[e][t] * sumz_m[e][t];
            sumz_m[e][t] = (sumz_m[e][t] * nz_t[e][t] + x) / (nz_t[e][t] + 1);
            nz_t[e][t] ++;
            sumz_s[e][t] = (sumz_s[e][t] - nz_t[e][t] * sumz_m[e][t] * sumz_m[e][t]) / nz_t[e][t];
        }
    }
    return 0;
}

int             Model::GibbsSampling(int maxIter, int BURN_IN, int SAMPLE_LAG)
{
    printf("####################\n");
    printf("Start Learning!\n");
    srand(745623);
    Init();
    int sample_cnt = 0;
    sum_lambda = new double[roleNum];
    sum_rho = new double[roleNum];
    sum_mu = new double*[roleNum];
    sum_delta = new double*[roleNum];
    for (int r = 0; r < roleNum; r ++)
    {
        sum_lambda[r] = 0.0;
        sum_rho[r] = 0.0;
        sum_mu[r] = new double[K];
        sum_delta[r] = new double[K];
        for (int t = 0; t < K; t ++)
        {
            sum_mu[r][t] = 0.0;
            sum_delta[r][t] = 0.0;
        }
    }
    for (int iter = 1; iter <= maxIter; iter ++)
    {
        printf("[Iteration %d]...\n", iter);
        int s1 = SampleDiffusion();
        if (s1 == -1)
        {
            printf("Error when sampling diffusion process!\n");
            return -1;
        }
        SampleFeature();
        if (iter < BURN_IN)
            continue;
        if ((iter - BURN_IN) % SAMPLE_LAG != 0)
            continue;
        sample_cnt ++;
        // update parameters
        for (unsigned int u = 0; u < nodeList.size(); u ++)
        {
            double sum = 0;
            for (int r = 0; r < roleNum; r ++)
            {
                theta[u][r] += (nur[u][r] + alpha + 0.0) / (nu[u] + roleNum * alpha);
                sum += theta[u][r];
            }
            /*
            if (sum != sample_cnt)
            {
                for (int r = 0; r < roleNum; r ++)
                {
                    printf("%d %d %.5lf\n", nur[u][r], nu[u], theta[u][r]);
                }
                return -1;
            }
            */
        }
        for (int r = 0; r < roleNum; r ++)
        {
            lambda[r] = (nr[r] + beta_0) / (sumt_r[r] + beta_0 + beta_1);
            rho[r] = (nrz[r][1] + gamma_1) / (nr[r] + gamma_0 + gamma_1);
            for (int t = 0; t < K; t ++)
            {
                mu[r][t] = (tau0 * tau1 + nz_t[r][t] * sumz_m[r][t]) / (tau1 + nz_t[r][t]);
                delta[r][t] = (2 * tau2 + nz_t[r][t]) / (2 * tau3 + nz_t[r][t] * sumz_s[r][t] + (tau1 * nz_t[r][t] * pow(sumz_m[r][t] - tau0, 2)) / (tau1 + nz_t[r][t]));
            }
        }
        PrintRho();
        PrintNr();
        PrintMu();
        for (int r = 0; r < roleNum; r ++)
        {
            sum_lambda[r] += lambda[r];
            sum_rho[r] += rho[r];
            for (int t = 0; t < K; t ++)
            {
                sum_mu[r][t] += mu[r][t];
                sum_delta[r][t] += delta[r][t];
            }
        }
    }

    for (unsigned int u = 0; u < nodeList.size(); u ++)
    {
        for (int r = 0; r < roleNum; r ++)
            theta[u][r] /= (sample_cnt + 0.0);
    }
    for (int r = 0; r < roleNum; r ++)
    {
        lambda[r] = sum_lambda[r] / sample_cnt;
        rho[r] = sum_rho[r] / sample_cnt;
        for (int t = 0; t < K; t ++)
        {
            mu[r][t] = sum_mu[r][t] / sample_cnt;
            delta[r][t] = sum_delta[r][t] / sample_cnt;
            delta[r][t] = sqrt(1.0 / delta[r][t]);
        }
    }
    printf("########## Final Parameters ##########\n");
    PrintRho();
    PrintMu();
    return 0;
}

int             Model::SaveTheta()
{
    FILE* fout = fopen("model_theta.txt", "w");
    for (int v = 0; v < V; v ++)
    {
        fprintf(fout, "%s\n", nodeList[v] -> name.c_str());
        for (int r = 0; r < roleNum; r ++)
            fprintf(fout, "%.5lf ", theta[v][r]);
        fprintf(fout, "\n");
    }
    fclose(fout);
    return 0;
}

int             Model::SaveGaussian()
{
    FILE* fout = fopen("model_gaussian.txt", "w");
    fprintf(fout, "Mean:\n");
    for (int r = 0; r < roleNum; r ++)
    {
        for (int t = 0; t < K; t ++)
        {
            fprintf(fout, "%.5lf ", mu[r][t]);
        }
        fprintf(fout, "\n");
    }
    fprintf(fout, "Deviation:\n");
    for (int r = 0; r < roleNum; r ++)
    {
        for (int t = 0; t < K; t ++)
            fprintf(fout, "%.5lf ", delta[r][t]);
        fprintf(fout, "\n");
    }
    fclose(fout);
    return 0;

}

int             Model::SaveRho()
{
    FILE* fout = fopen("model_rho.txt", "w");
    fprintf(fout, "Rho:\n");
    for (int r = 0; r < roleNum; r ++)
        fprintf(fout, "%.10lf ", rho[r]);
    fprintf(fout, "\nLambda:\n");
    for (int r = 0; r < roleNum; r ++)
        fprintf(fout, "%.10lf ", lambda[r]);
    fprintf(fout, "\n");
    fclose(fout);
    return 0;
}

int             Model::Save(string fileDir)
{
    SaveTheta();
    SaveRho();
    SaveGaussian();
    FILE* fout = fopen(fileDir.c_str(), "w");
    for (int r = 0; r < roleNum; r ++)
        fprintf(fout, "%.10lf ", rho[r]);
    fprintf(fout, "\n");
    for (int r = 0; r < roleNum; r ++)
        fprintf(fout, "%.10lf ", lambda[r]);
    fprintf(fout, "\n");
    for (int r = 0; r < roleNum; r ++)
    {
        for (int t = 0; t < K; t ++)
        {
            fprintf(fout, "%.10lf ", mu[r][t]);
        }
        fprintf(fout, "\n");
    }
    for (int r = 0; r < roleNum; r ++)
    {
        for (int t = 0; t < K; t ++)
            fprintf(fout, "%.10lf ", delta[r][t]);
        fprintf(fout, "\n");
    }
    for (int v = 0; v < V; v ++)
    {
        for (int r = 0; r < roleNum; r ++)
            fprintf(fout, "%.10lf ", theta[v][r]);
        fprintf(fout, "\n");
    }
    fclose(fout);
    return 0;
}

int                 Model::PrintNr()
{
    printf("#sampled roles:\n");
    for (int r = 0; r < roleNum; r ++)
        printf("%d ", nr[r]);
    printf("\n");
    return 0;
}

int                 Model::PrintTheta()
{
    for (int v = 0; v < V; v ++)
    {
        for (int r = 0; r < roleNum; r ++)
            printf("%.5lf ", theta[v][r]);
        printf("\n");
    }
    return 0;
}

int                 Model::PrintRho()
{
    printf("Rho: ");
    for (int r = 0; r < roleNum; r ++)
    {
        printf("%.8lf ", rho[r]);
    }
    printf("\nLambda: ");
    for (int r = 0; r < roleNum; r ++)
    {
        printf("%.8lf ", lambda[r]);
    }
    printf("\n");
    return 0;
}

int                 Model::PrintMu()
{
    printf("Mu:\n");
    for (int r = 0; r < roleNum; r ++)
    {
        for (int k = 0; k < K; k ++)
        {
            printf("%.8lf ", mu[r][k]);
        }
        printf("\n");
    }
    printf("Delta: \n");
    for (int r = 0; r < roleNum; r ++)
    {
        for (int k = 0; k < K; k ++)
            printf("%.8lf ", delta[r][k]);
        printf("\n");
    }
    return 0;
}

bool                SecondCmp(pair<int, double> a, pair<int, double> b)
{
    return a.second < b.second;
}

int                 Model::RoleLevelTest()
{
    printf("Role-level test!\n");
    set<int>* truth = new set<int>[S];
    vector<pair<int, double> >** res = new vector<pair<int, double> >*[roleNum];
    for (int r = 0; r < roleNum; r ++)
    {
        res[r] = new vector<pair<int, double> >[S];
        for (int v = 0; v < V; v ++)
            for (int s = 0; s < S; s ++)
                res[r][s].push_back(make_pair(v, 1.0));
    }
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        int sid = post -> sourceId;
        int u = post -> user -> id;
        Node* user = post -> user;
        if (post -> sourcePost -> id != post -> id)
            truth[sid].insert(user -> id);
        for (unsigned int j = 0; j < user -> inEdgeList.size(); j ++)
        {
            Node* target = user -> inEdgeList[j];
            int v = user -> inEdgeList[j] -> id;
            int pid = target -> GetPostIdBySource(post -> sourcePost -> id);
            int tiv = MAXINT;
            if (pid != -1)
                tiv = postList[pid] -> postTime;
            if (pid != -1 && tiv < post -> postTime)
                continue;
            double prob = 0.0;
            int role = 0;
            for (int r = 0; r < roleNum; r ++)
            {
                prob += (rho[r] * pow(1 - lambda[r], maxTime - 1) + (1 - rho[r])) * theta[u][r];
                if (theta[v][r] > theta[v][role])
                    role = r;
            }
            res[role][sid][v].second *= prob;
        }
    }
    int posCnt = 0;
    int allCnt = 0;
    for (int s = 0; s < S; s ++)
    {
        posCnt += truth[s].size();
        allCnt += res[0][s].size();
    }
    printf("Average Postive Instance: %.5lf\n", (posCnt + 0.0) / (S + 0.0));
    printf("Postive : Negative Instance: %.5lf\n", (posCnt + 0.0) / (allCnt - posCnt));
   
    int* C = new int[roleNum];
    int testCase = 0;
    for (int r = 0; r < roleNum; r ++)
    {
        printf("Role: %d\n", r);
        C[r] = 0;
        double map = 0.0;
        double mrr = 0.0;
        double* P = new double[100];
        for (int i = 0; i < 100; i ++)
            P[i] = 0.0;
        for (int s = 0; s < S; s ++)
            truth[s].clear();
        for (unsigned int i = 0; i < postList.size(); i ++)
        {
            Post* post = postList[i];
            int sid = post -> sourceId;
            int u = post -> user -> id;
            Node* user = post -> user;
            int role = 0;
            for (int rr = 0; rr < roleNum; rr ++)
                if (theta[u][rr] > theta[u][role])
                    role = rr;
            if (post -> sourcePost -> id != post -> id && role == r)
                truth[sid].insert(u);
        }
        for (int s = 0; s < S; s ++)
        {
            C[r] += res[r][s].size();
            sort(res[r][s].begin(), res[r][s].end(), SecondCmp);
            double ap = 0.0;
            double ar = 0.0;
            int hitCnt = 0;
            for (unsigned int i = 0; i < res[r][s].size(); i ++)
            {
                int v = res[r][s][i].first;
                int hit = 0;
                if (truth[s].count(v) > 0)
                    hit ++;
                hitCnt += hit;
                if (hit > 0)
                {
                    ap += (hitCnt + 0.0) / (i + 1.0);
                    ar += 1.0 / (i + 1.0);
                }
                //ap += (hitCnt + 0.0) / (i + 1.0);
                if (i < 100)
                    P[i] += hit;
                //ap += (hit + 0.0) / (i + 1.0);
                //mrr += (hitCnt + 0.0) / (i + 1.0);
            }
            if (truth[s].size() > 0)
            {
                map += ap / truth[s].size();
                mrr += ar / truth[s].size(); 
            }
            testCase += truth[s].size();
        }
        for (int i = 0; i < 100; i ++)
            P[i] += P[i - 1];
        for (int i = 0; i < 100; i ++)
            P[i] /= ((i + 1.0) * S);
        map /= S;
        mrr /= S;
        printf("P@1: %.5lf\n", P[0]);
        printf("P@3: %.5lf\n", P[2]);
        printf("P@5: %.5lf\n", P[4]);
        printf("P@10: %.5lf\n", P[9]);
        printf("P@20: %.5lf\n", P[19]);
        printf("P@50: %.5lf\n", P[49]);
        printf("P@100: %.5lf\n", P[99]);
        printf("MAP: %.5lf\n", map);
        printf("MRR: %.5lf\n", mrr);
    }

    int allC = 0;
    for (int r = 0; r < roleNum; r ++)
        allC += C[r];
    for (int r = 0; r < roleNum; r ++)
    {
        printf("%.5lf ", (C[0] + 0.0) / allC);
    }
    printf("\n");
    return 0;
}

int                 Model::Test()
{
    printf("Post-level test!\n");
    set<int>* truth = new set<int>[S];
    vector<pair<int, double> >* res = new vector<pair<int, double> >[S];
    for (int s = 0; s < S; s ++)
    {
        truth[s].clear();
        for (int v = 0; v < V; v ++)
            res[s].push_back(make_pair(v, 1.0));
    }
    for (unsigned int i = 0; i < postList.size(); i ++)
    {
        Post* post = postList[i];
        int sid = post -> sourceId;
        int u = post -> user -> id;
        Node* user = post -> user;
        if (post -> sourcePost -> id != post -> id)
            truth[sid].insert(user -> id);
        for (unsigned int j = 0; j < user -> inEdgeList.size(); j ++)
        {
            Node* target = user -> inEdgeList[j];
            int v = user -> inEdgeList[j] -> id;
            int pid = target -> GetPostIdBySource(post -> sourcePost -> id);
            int tiv = MAXINT;
            if (pid != -1)
                tiv = postList[pid] -> postTime;
            if (pid != -1 && tiv < post -> postTime)
                continue;
            double prob = 0.0;
            double maxProb = 0.0;
            int maxR;
            for (int r = 0; r < roleNum; r ++)
            {
                prob += (rho[r] * pow(1 - lambda[r], maxTime - 1) + (1 - rho[r])) * theta[u][r];
                if (theta[u][r] > maxProb)
                {
                    maxProb = theta[u][r];
                    maxR = r;
                }
            }
            prob = rho[maxR] * pow(1 - lambda[maxR], maxTime - 1) + (1 + rho[maxR]);
            res[sid][v].second *= prob;
        }
    }
    int posCnt = 0;
    int allCnt = 0;
    for (int s = 0; s < S; s ++)
    {
        posCnt += truth[s].size();
        allCnt += res[s].size();
    }
    printf("Average Postive Instance: %.5lf\n", (posCnt + 0.0) / (S + 0.0));
    printf("Postive : Negative Instance: %.5lf\n", (posCnt + 0.0) / (allCnt - posCnt));
    double map = 0.0;
    double mrr = 0.0;
    int testCnt = 0;
    double* P = new double[100];
    for (int i = 0; i < 100; i ++)
        P[i] = 0.0;
    printf("#query : %d\n", S);
    for (int s = 0; s < S; s ++)
    {
        sort(res[s].begin(), res[s].end(), SecondCmp);
        //if (s == 0)
        //    printf("%.10lf %.10lf\n", res[s][0].second, res[s][1].second);
        double ap = 0.0;
        double ar = 0.0;
        int hitCnt = 0;
        for (unsigned int i = 0; i < res[s].size(); i ++)
        {
            int v = res[s][i].first;
            int hit = 0;
            if (truth[s].count(v) > 0)
                hit ++;
            hitCnt += hit;
            if (hit > 0)
            {
                //if (s == 0)
                //    printf("%d ", i);
                ap += (hitCnt + 0.0) / (i + 1.0);
                ar += 1.0 / (i + 1.0);
            }
            //ap += (hitCnt + 0.0) / (i + 1.0);
            if (i < 100)
                P[i] += hit;
            //ap += (hit + 0.0) / (i + 1.0);
            //mrr += (hitCnt + 0.0) / (i + 1.0);
        }
        map += ap / truth[s].size();
        mrr += ar / truth[s].size();
        //if (s == 0)
        //    printf("\nMAP: %.5lf\n", ap / truth[s].size());
        testCnt += truth[s].size();
    }
    for (int i = 0; i < 100; i ++)
        P[i] += P[i - 1];
    for (int i = 0; i < 100; i ++)
        P[i] /= ((i + 1.0) * S);
    map /= S;
    mrr /= S;
    printf("#Test cases: %d\n", testCnt);
    printf("P@1: %.5lf\n", P[0]);
    printf("P@3: %.5lf\n", P[2]);
    printf("P@5: %.5lf\n", P[4]);
    printf("P@10: %.5lf\n", P[9]);
    printf("P@20: %.5lf\n", P[19]);
    printf("P@50: %.5lf\n", P[49]);
    printf("P@100: %.5lf\n", P[99]);
    printf("MAP: %.5lf\n", map);
    printf("MRR: %.5lf\n", mrr);
    return 0;
}

