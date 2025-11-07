#  This repo will contain the lfs ml-models for all the commodities

# Enable git-flow
   ```
     sudo apt-get install git-flow
     git clone https://github.com/agshift/ml-models.git
     cd ml-models
     git flow init
         (Keep accepting the default selections)
   ```

# Install git lfs
  * Ref: https://github.com/git-lfs/git-lfs/wiki/Installation
    ```
       * curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
       * sudo apt-get install git-lfs
    ```
  
# Setup git lfs for the desired repo
  * Ref: https://git-lfs.github.com/
  * **It's important to do this being in the local repo directory**
  * ***Copy the commodity models under [ml-models/commodity-name/graph_name/1]***
   ```
       cd ml-models
       git config user.name your-GitHub-user-name
       git config user.email your-GitHub-user-email@something.com
       git lfs install
       git lfs track "*.pb"
       git lfs track
       git add .gitattributes
       git diff --cached
       git commit -m "Track .pb files with Git LFS"
       git add .
       git commit -m "added .pb file"
       git push
       git push origin develop
   ```

# Cloning git lfs repo
```sh
GIT_LFS_SKIP_SMUDGE=1 git clone git@github.com:agshift/ml-models.git
cd ml-models
git lfs pull
```

# Raspberry:

* Models are under the directory: raspberry
  * MaskRCNN: raspberry/raspberry_seg_mrcnn_graph

