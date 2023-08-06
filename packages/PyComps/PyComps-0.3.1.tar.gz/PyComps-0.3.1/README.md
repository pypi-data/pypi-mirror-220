# PyComps

Easy calculation of composite properties


## Brief description


A Python toolbox for the structural analysis of orthotropic layered components. 
The program implements both the micro and meso/macro mechanics in the classes *"PlyDef"* and *"Laminate"*.
Class methods allow different operations. 

### **Laminate** - meso/macro mechanics


creates a laminate object starting from the plies properties and stack-up information. 

Features:

- calculation of the laminate **stiffness matrix**
- estimation of **equivalent** tensile and flexural **orthotropic** mechanical **properties**. 
- **ply-by-ply stress** analysis in accordance with CLT or FSDT. 
- Failure verification with **maximum stress**, **maximum strain** and **Tsai-Wu** criteria

### **PlyDef** - micro mechanics

manipulation of ply objects generated from the constituents' properties and mass or volume fractions. 

Features:

- calculation of **ply mechanical properties** starting from that of isotropic constituents.
- the former can be attained with different methods: **ROM**, **Halpin-Tsai**, or **PMM**
- **cured ply thickness** estimation


### Source Code: 
https://github.com/edo-147/PyComp

### notes: 
aligned with GitHub tag v0.3.0