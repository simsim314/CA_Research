This is sparse 3d cellular automata rule filter and simulator. It runs as golly script.  

The visualization is using 4 projections for each point (x, y, z): 
1. xy 
2. yz
3. xz 
4. (x + y + z, -x + y + z). 

To search for new interesting rules just run CA3dRuleSearch.py in golly. 

To use the existing rules and patterns:
1. copy '3d' folder of this repository into golly folder ('files' folder of golly). 
2. Run CA3dSimulator.py
3. For help press 'h' 

Important notes: 

- To load rule just press 'l' and state the rule index - just enter number. 
- To load pattern press 'p' and name file saved without the pat prefix and .pkl suffix. 
For example to load patGldOsc33.pkl enter the name: GldOsc33
