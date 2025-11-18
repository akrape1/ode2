#include <TCanvas.h>
#include <TGraph.h>
#include <TMultiGraph.h>
#include <TAxis.h>
#include <TLegend.h>
#include <cmath>
#include "RK.hpp"

// ODE: y' = 10y
double f(double x, double y) {
    return 10*y;
}

// Exact solution y(x) = exp(10x)
double yexact(double x) {
    return exp(10*x);
}

void RKtest() {

    int nsteps = 50;
    double x0 = 0.0;

    // IMPORTANT: choose xmax < 1 (blow-up point)
    double xmax = 0.9;

    double y0 = 1.0;

    // Run solvers
    TGraph gRK1 = RK1Solve(f, y0, nsteps, x0, xmax);
    TGraph gRK2 = RK2Solve(f, y0, nsteps, x0, xmax);
    TGraph gRK4 = RK4Solve(f, y0, nsteps, x0, xmax);

    // Exact
    TGraph gExact;
    for (int i = 0; i < nsteps; i++) {
        double x = x0 + i*(xmax-x0)/nsteps;
        gExact.SetPoint(i, x, yexact(x));
    }

    // Style
    gExact.SetLineColor(kBlack);
    gExact.SetLineWidth(3);

    gRK1.SetLineColor(kRed);
    gRK1.SetLineWidth(2);

    gRK2.SetLineColor(kBlue);
    gRK2.SetLineWidth(2);

    gRK4.SetLineColor(kGreen+2);
    gRK4.SetLineWidth(2);

    // Plot
    TCanvas *c1 = new TCanvas("c1","RK Comparison",1200,800);

    TMultiGraph *mg = new TMultiGraph();
    mg->Add(&gExact);
    mg->Add(&gRK1);
    mg->Add(&gRK2);
    mg->Add(&gRK4);

    mg->SetTitle("y' = 10y; x; y");
    mg->Draw("AL");

    TLegend *leg = new TLegend(0.7,0.7,0.9,0.9);
    leg->AddEntry(&gExact,"Exact","l");
    leg->AddEntry(&gRK1,"RK1","l");
    leg->AddEntry(&gRK2,"RK2","l");
    leg->AddEntry(&gRK4,"RK4","l");
    leg->Draw();

    c1->Update();
    c1->SaveAs("./RK4.pdf");
}
