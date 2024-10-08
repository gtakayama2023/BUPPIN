#include <iostream>
#include <fstream>
#include <cmath>
#include <vector>
#include <iomanip>

using namespace std;

void writeData(ofstream& outFile, double XX, double TH, double WeightedTH, double binContent) {
    outFile << XX << " " << TH << " " << WeightedTH << " " << binContent << endl;
}

double calculateWeightedAverage(int events, double totalWeightedValue) {
    return totalWeightedValue / events;
}

int main() {
    ofstream outFile("target/thick/thick.dat");
    ofstream outFile2("target/Wthick/Wthick.dat");
    ofstream outFile3("target/F5X/F5X.dat");

    // 各データのサイズを取得
    const int SZ = sizeof(arX) / sizeof(arX[0]);

    // X軸の範囲とビン数
    double maxX = h->GetXaxis()->GetXmax();
    double minX = h->GetXaxis()->GetXmin();
    int nn = h->GetNbinsX();
    int mm = nn + 1; 

    // 平均値の計算用変数
    double weightedAverageTH = 0.;
    double weightedAverageTHerr = 0.;
    int events = 0;

    if (minX > -100.0 && maxX < 98.0 && nn > 0) {
        for (int i = 1; i < mm; i++) {
            double XX = i * (maxX - minX) / nn + minX;
            int ii = floor(XX / 2.0 + 50.0);
            double TH = (XX - (ii * 2.0 - 100.0)) * (arT[ii + 1] - arT[ii]) / 2.0 + arT[ii];
            double binContent = h->GetBinContent(i);
            double weightedTH = binContent * TH;
            double THerr = (XX - (ii * 2.0 - 100.0)) * (arTerr[ii + 1] - arTerr[ii]) / 2.0 + arTerr[ii];
            double weightedTHerr = binContent * THerr;

            writeData(outFile, XX, TH, weightedTH, binContent);
            outFile2 << XX << " " << weightedTH << endl;
            outFile3 << XX << " " << binContent << endl;

            weightedAverageTH += weightedTH;
            weightedAverageTHerr += weightedTHerr;
            events += binContent;
        }

        weightedAverageTH = calculateWeightedAverage(events, weightedAverageTH);
        weightedAverageTHerr = calculateWeightedAverage(events, weightedAverageTHerr);

        cout << "===========================================================" << endl;
        cout << "Weighted ave. thickness(g/cm2) = " << setprecision(4) << weightedAverageTH
             << " +- " << setprecision(4) << weightedAverageTHerr << endl;
        cout << "Relative error = " << setprecision(3) << (weightedAverageTHerr / weightedAverageTH) * 100.0 << " %" << endl;
        cout << "Total Events = " << events << endl;
        cout << "===========================================================" << endl;
    } else {
        cout << "Make F5X plot Xmin>-100. and Xmax<98." << endl;
    }

    return 0;
}

