# Implementation planning
## Modules: 
- Storage of user data
- Reading user data from file
- Graphing user data
## Dependencies:
In order to graph data, the data must be read, and in order to be read from a file, the data must first be written to a file. Hence I will first develop the storage of user data module such that while developing the other two I am able to integrate the base function.

# Testing strategies
- One method of testing I will employ is RGB testing, in order to ensure that the program fits to the desired requirements without doing too much.
- Another one I will use is edge testing, wherein I perform edge cases and determine the limits of the program. This will aid me in discovering bugs or flaws within the code, and allow me to determine where to improve my system.

# Maintenance considerations
Examples where this code will need maintaining in the future include if mark or ranking systems in school change or if there becomes another method of determining academic success (For example if mark divided by rank became measured)
I could improve the maintainability of the code by creating in depth comments on internal documentation explaining the purpose and function of code. I could also ensure to keep all functions contained within modules to allow interchangeability and simple rearranging of necessary functions, and I could name functions in such a way as to keep them differentiable.

# Social and ethical
One potential social consideration is that evaluating success by numerical data can be seen as labelling and reductive of student's efforts, which may cause offence to or upset users. To counteract this, numerical data must not be associated with success, and rather simply show results. This affects the user interface and data storage practices.