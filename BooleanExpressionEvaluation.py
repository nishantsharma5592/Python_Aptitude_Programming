# A simulation of evaluation of boolean expressions
# We build up classes in increasing order of complexity

# Basic boolean class
class Boolean:
    def __init__(self, _value):
        self.value = _value
    def getValue(self):
        return self.value
    def setValue(self, new_value):
        self.value = new_value 

# Boolean variable class
class BooleanVariable:
    def __init__(self, _name):
        self.name = _name
        self.boolean = None
    def getBoolean(self):
        return self.boolean
    def setBoolean(self, boolean_object):
        self.boolean = boolean_object

# This is of the type AND, OR, and NOT
class BasicBooleanOperator:
    def __init__(self, reference, _left_bool_var, _right_bool_var):
        self.reference = reference
        self.left_boolean_variable = _left_bool_var
        self.right_boolean_variable = _right_bool_var
        self.boolean = None # This is the answer

    def apply(self):
        if self.reference == "NOT":
            self.boolean = Boolean(not\
                    self.left_boolean_variable.getBoolean().getValue())
        elif self.reference == "AND":
            self.boolean = \
                    Boolean(self.left_boolean_variable.getBoolean().getValue()\
                    and self.right_boolean_variable.getBoolean().getValue())
        elif self.reference == "OR":
            self.boolean = \
                    Boolean(self.left_boolean_variable.getBoolean().getValue()\
                    or self.right_boolean_variable.getBoolean().getValue())
        else:
            print("Unrecognized reference!")
    
    def getBoolean(self):
        return self.boolean

# The complex boolean operator class may require services of the basic boolean
# operator class
class ComplexBooleanOperator:
    def __init__(self, reference, _left_bool_var, _right_bool_var):
        self.reference = reference
        self.left_boolean_variable = _left_bool_var
        self.right_boolean_variable = _right_bool_var
        self.boolean = None # This is the answer

    def apply(self):
        if self.reference == "IMPLY":
            basic_boolean_operand_1 = BasicBooleanOperator("NOT", \
                    self.left_boolean_variable, None)
            basic_boolean_operand_1.apply()
            basic_boolean_operand_1_value =\
                    basic_boolean_operand_1.getBoolean().getValue()
            boolean_variable_2_value = \
                    self.right_boolean_variable.getBoolean().getValue()
            self.boolean = Boolean(basic_boolean_operand_1_value or \
                    boolean_variable_2_value)
        elif self.reference == "DOUBLE IMPLY":
            # We call help from the same class in which we
            # are being set up
            # The first side of implication
            imply_a_b = ComplexBooleanOperator("IMPLY", a, b)
            imply_a_b.apply()
            bool_left = imply_a_b.getBoolean().getValue()
            # The other side of implication 
            imply_b_a = ComplexBooleanOperator("IMPLY", b, a)
            imply_b_a.apply()
            bool_right = imply_b_a.getBoolean().getValue()

            self.boolean = Boolean(bool_left and bool_right)
            
        else:
            print("Unrecognized reference!")
    
    def getBoolean(self):
        return self.boolean

if __name__ == "__main__":
    true = Boolean(True)
    false = Boolean(False)
    
    print("Value of true:", true.getValue())
    print("Value of false:", false.getValue())

    a = BooleanVariable("A")
    b = BooleanVariable("B")
    
    # Set 1
    # a.setBoolean(true)
    # b.setBoolean(true)

    # Set 2
    # a.setBoolean(true)
    # b.setBoolean(false)
    
    # Set 3
    # a.setBoolean(false)
    # b.setBoolean(true)

    # Set 4
    a.setBoolean(false)
    b.setBoolean(false)

    print("Value of A:", a.getBoolean().getValue())
    print("Value of B:", b.getBoolean().getValue())

    not_a = BasicBooleanOperator("NOT", a, None)
    not_a.apply()
    print("Value of NOT A:", not_a.getBoolean().getValue())

    and_a_b = BasicBooleanOperator("AND", a, b)
    and_a_b.apply()
    print("Value of A AND B:", and_a_b.getBoolean().getValue())

    or_a_b = BasicBooleanOperator("OR", a, b)
    or_a_b.apply()
    print("Value of A OR B:", or_a_b.getBoolean().getValue())

    imply_a_b = ComplexBooleanOperator("IMPLY", a, b)
    imply_a_b.apply()
    print("Value of A => B:", imply_a_b.getBoolean().getValue())
    
    double_imply_a_b = ComplexBooleanOperator("DOUBLE IMPLY", a, b)
    double_imply_a_b.apply()
    print("Value of A <=> B:", double_imply_a_b.getBoolean().getValue())

