class Structure:
  def __init__(self, structureType):
    self.structureType = structureType

# Class for Element---------------------------------------------------------------------------
class Element:
  def __init__(self, elementNumber,  initialNode, finalNode, length, elasticModulus, shearModulus, csArea, planarInertia, polarInertia, constant, constant1, constant2, constant3, constant4, constant5, sinElement, cosElement):
    self.elementNumber = elementNumber
    self.initialNode = initialNode
    self.finalNode = finalNode
    self.length = length
    self.elasticModulus = elasticModulus
    self.shearModulus = shearModulus
    self.csArea = csArea
    self.planarInertia = planarInertia
    self.polarInertia = polarInertia
    self.constant = constant
    self.constant1 = constant1
    self.constant2 = constant2
    self.constant3 = constant3
    self.constant4 = constant4
    self.constant5 = constant5
    self.sinElement = sinElement
    self.cosElement = cosElement
# Class for Element (End)------------------------------------------------------------------------

# Class for Coordinate (Start)-------------------------------------------------------------------
class Coordinate:
  def __init__(self, nodeNumber:int, cox:float=0, coy:float=0, coz:float=0):
    self.nodeNumber = nodeNumber
    self.cox = cox
    self.coy = coy
    self.coz = coz
# Class for Coordinate (End)---------------------------------------------------------------------

# Class for Load (Start)----------------------------------------------------------------------
class Support:
  def __init__(self, supportNumber, supportType, supportNode):
    self.supportNumber = supportNumber
    self.supportType = supportType
    self.supportNode = supportNode
# Class for Support (End))-----------------------------------------------------------------------

# Class for Load (Start))------------------------------------------------------------------------
class Load:
  def __init__(self, loadNumber, loadType, loadNode, loadMagnitude):
    self.loadNumber = loadNumber
    self.loadType = loadType
    self.loadNode = loadNode
    self.loadMagnitude = loadMagnitude
# Class for Load (End))--------------------------------------------------------------------------

# class Nodes:
#   nodes = {}

#   def __init__(self):
#     """
#     1 - Vertical
#     2 - Horizontal
#     3 - Moment
#     4 - Distributed Load [R]
#     5 - Distributed Load [RT]
#     6 - Distributed Load [IT]
#     7 - Distributed Load [P]
#     8 - Concentrated Load [1]
#     9 - Concentrated Load [2]
#     10 - Concentrated Load [3]
#     """
#     self.type_load = ['V', 'H', 'M', 'R', 'RT', 'IT', 'P', 'C1', 'C2', 'C3']

#   def add_load(self, position:int, type_load:int = 1, magnitude = 0, a = 0, b = 0, alpha = 0, P = 0):
#     if type_load <= 3:
#       new_load = {
#         self.type_load[type_load - 1]: {
#           position: {
#             "magnitude": magnitude
#           }
#         }
#       }
#     elif type_load <= 7:
#       new_load = {
#         self.type_load[type_load - 1]: {
#           position: {
#             "magnitude": magnitude
#           }
#         }
#       }
#     if position in Nodes.nodes:
#       Nodes.nodes[position].update(new_load[position])
#       return
#     Nodes.nodes.update(new_load)

# if __name__ == "__main__":
#   node = Nodes()

#   node.add_load(2, 1, 10000.5)
#   node.add_load(2, 2, -8.5)
#   node.add_load(5, 3, 5.5)
#   print(Nodes.nodes)
#   print()

#   print(node.nodes.keys())
#   print()

#   for load in node.nodes.keys():
#     print(node.nodes[load])
#   print()

#   for load in node.nodes.keys():
#     print(node.nodes[load].keys())
#   print()

#   print(node.nodes[2])
#   print()

#   print(node.nodes[2]['vertical'])