# change the version number
#bash -c 'sed -i "s/Version\: 0\.5\.[0987654321]\{1,20\}/Version: 0.5."$(git log --pretty=oneline --all | wc -l)"/g" .debdata/control'
bash -c 'sed -i "s/Version\: 0\.5\.[0987654321]\{1,20\}/Version: 0.5."$(git log --pretty=oneline --all | wc -l)"/g" debian/DEBIAN/control'
# change the packagesize to however big the build is now
#bash -c 'sed -i "s/Size\: [0987654321]\{1,20\}/Size: "$(cat packageSize.txt)"/g" .debdata/control'
bash -c 'sed -i "s/Size\: [0987654321]\{1,20\}/Size: "$(cat packageSize.txt)"/g" debian/DEBIAN/control'
