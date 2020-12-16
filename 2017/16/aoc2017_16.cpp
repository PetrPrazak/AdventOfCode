#include <algorithm>
#include <iostream>
#include <sstream>
#include <vector>

using namespace std;

vector<string> split( const string& s, const string& delimiter )
{
	size_t pos_start = 0, pos_end, delim_len = delimiter.length();
	string token;
	vector<string> res;
	while ( ( pos_end = s.find( delimiter, pos_start ) ) != string::npos )
	{
		token = s.substr( pos_start, pos_end - pos_start );
		pos_start = pos_end + delim_len;
		res.push_back( token );
	}
	res.push_back( s.substr( pos_start ) );
	return res;
}

void dance(string row, const vector<string> & moves, int repeat = 1)
{
    vector<string> visits;
    for (int cycle = 0; cycle < repeat; ++cycle)
    {
        if (find(visits.begin(), visits.end(), row) != visits.end()) 
        {
            cout << cycle << " " << visits[repeat % cycle] << "\n";
            return;
        }
        visits.push_back(row);
        for ( auto& move : moves )
        {
            stringstream ss( move );
            char cmd;
            ss >> cmd;
            if ( cmd == 's' )
            {
                int cnt;
                ss >> cnt;
                rotate( row.begin(), row.end() - cnt, row.end() );
            }
            else if ( cmd == 'x' )
            {
                int a, b;
                ss >> a >> cmd >> b;
                swap( row[a], row[b] );
            }
            else if ( cmd == 'p' )
            {
                char a, b;
                ss >> a >> cmd >> b;
                int x = row.find( a );
                int y = row.find( b );
                swap( row[x], row[y] );
            }
        }
    }
    cout << row << '\n'; // for part 1
}

string init_row()
{
	string row;
	row.reserve( 16 );
	for ( char c = 'a'; c <= 'p'; ++c )
	{
		row += c;
	}
    return row;
}

int main()
{
	string data;
	cin >> data;
	vector<string> moves = split( data, "," );
    // cout << moves.size() << '\n';
    string row = init_row();
    dance(row, moves);
    dance(row, moves, 1000000000);
	return 0;
}
