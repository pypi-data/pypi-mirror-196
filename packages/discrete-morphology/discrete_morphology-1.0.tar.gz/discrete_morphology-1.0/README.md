# Discrete Morphology

A library written in pure Python for computing morphological operators using discrete connectives. Although mathematical morphology operators are usually defined on the interval $[0,1]$, grey-level images take discrete values when stored in a computer, usually on the finite chain $L_{255}=\lbrace 0,1,\dots, 255 \rbrace$. To this end, the following reference establishes a framework in which operators equivalent to the $[0,1]$ operators but for the finite chain $L_n$ are proposed:
```
González-Hidalgo M., Massanet S.
A fuzzy mathematical morphology based on discrete t-norms: fundamentals and applications to image processing.
Soft Computing, 18 (11), 2014, 2297–2311. https://doi.org/10.1007/s00500-013-1204-6
``` 

Since the methods depend on connectives defined on the finite chain L_n, in [DiscreteFuzzyOperators](https://github.com/mmunar97/discrete-fuzzy-operators) there is a library devoted to the implementation of these operators, as well as a study of their properties. For more information on these discrete operators, see:
```
Munar M., Massanet S., Ruiz-Aguilera D.
A review on logical connectives defined on finite chains.
Fuzzy Sets and Systems, 2023. https://doi.org/10.1016/j.fss.2023.01.004.
``` 