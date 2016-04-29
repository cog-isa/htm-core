#include <bits/stdc++.h>

using namespace std;

void out_wrap(vector<pair<int, int> > a) {
    cout << "[";
    for (int i = 0; i < (int) a.size(); i++)
        cout << "[" << a[i].first << ',' << a[i].second << "]," << endl;
    cout << "]";
}

int main() {
    string s;
    vector<pair<double, double> > a;
    while (getline(cin, s)) {
//        cout << s << endl;
        stringstream ss;
        ss << s;
        char buf;
        double x, y;
        ss >> buf >> x >> buf >> y;
        a.push_back(make_pair(x, y));
    }
    vector<pair<int, int> > b;
    for (int i = 0; i < (int) a.size(); i++) {
        int x = (int) (a[i].first / 5 + 0.5);
        int y = (int) (a[i].second / 5 + 0.5);
        if (b.size() == 0 || make_pair(x, y) != b[b.size() - 1])
            b.push_back(make_pair(x, y));
    }
    out_wrap(b);

    return 0;
}
