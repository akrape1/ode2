import ROOT as r

def RK1Solve(f, y0, nsteps, x0, xmax) -> r.TGraph:
  
    h=(xmax-x0)/nsteps     # step size
    x=x0                   # independent variable

    y=y0                   # dependent variable to plot vs x
    tg = r.TGraph()
    tg.SetPoint(0,x0,y0)   # initial condition	      
  
    for i in range(nsteps-1):
        k1 = h*f(x,y)
        y = y+k1
        x+=h
        tg.SetPoint(i+1,x,y)
    return tg


def RK2Solve(f, y0, nsteps, x0, xmax):

    h=(xmax-x0)/nsteps      # step size
    x=x0                    # independent variable
  
    y=y0                   # dependent variable to plot vs x
    tg=r.TGraph()
    tg.SetPoint(0,x0,y0)    # initial condition
	      
    for i in range(nsteps-1):
        k1 = h*f(x,y)
        k2 = h*f(x+h/2,y+k1/2)
        y  = y + k2
        x+=h
        tg.SetPoint(i+1,x,y)
    return tg



# the differential equation to be solved
def fun1(x, y):
    x=None               # unused variable
    return -2*y          # f = y'(x,y) = -2 * y(x)  
                         # solution: y(x) = 3 * exp(-2*x) ; with initial condition y(0)=3


# solve our DEQ using RK1 or RK2 methods!
# Two examples are given.  Choose a function for testing
tg1=RK1Solve(fun1,3,30,0,3)                      # initial condition y(0)=3
tg2=RK2Solve(fun1,3,30,0,3) 
fun_sol=r.TF1("fun_sol","3*exp(-2*x)",0,3)       # exact solution

# ******************************************************************************
# ** this block is useful for supporting both high and std resolution screens **
dh = r.TGClient.Instance().GetDisplayHeight()//2;   # fix plot to 1/2 screen height  
#UInt_t dw = gClient->GetDisplayWidth();
dw = int(1.1*dh)
# ******************************************************************************

c1 = r.TCanvas("c1","DEQ solutions",dw,dh)

tg1.SetMarkerSize(0.015*dh/8);  # size scale: 1 = 8 pixels, so here we choose the size to be 1.5% of the window height
tg2.SetMarkerSize(0.015*dh/8);
tg1.SetMarkerStyle(r.kFullTriangleUp);
tg2.SetMarkerStyle(r.kFullTriangleDown);
tg1.SetMarkerColor(r.kRed);
tg2.SetMarkerColor(r.kGreen-2);
fun_sol.SetLineColor(r.kBlack);
fun_sol.SetLineStyle(2);
  
# plot the results
tg1.SetTitle("ODE demo;x;y")
tg1.Draw("AP");
tg2.Draw("P");
fun_sol.Draw("same");
  
tl = r.TLegend(0.6,0.7,0.9,0.9);
tl.AddEntry(tg1,"RK1 Solution","p");
tl.AddEntry(tg2,"RK2 Solution","p");
tl.AddEntry(fun_sol,"Exact Solution","l");
tl.Draw()
c1.Draw()
c1.Update()
c1.Print("OED_py.png")

input("hit return to exit")
