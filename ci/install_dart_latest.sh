sudo apt-add-repository ppa:dartsim/ppa -y
sudo apt-get -qq update

sudo apt-get -qq --yes --force-yes install libccd-dev libfcl-dev

git clone git://github.com/dartsim/dart.git
cd dart
mkdir build
cd build
cmake -DCMAKE_BUILD_TYPE=Release ..
make -j4
sudo make install
# cd ..
# mkdir build_py
# cd build_py
# cmake -DDART_BUILD_DARTPY=ON -DCMAKE_BUILD_TYPE=Release ..
# make -j4
# sudo make install
sudo ldconfig
cd $CI_HOME
