

from vector3 	import Vector3
from matrix4 	import Matrix4
from quaternion	import Quaternion

class Transform:
	def __init__(self):

		self.position 		= Vector3()
		self.rotation		= Quaternion()
		self.scale			= Vector3()

		self.result_matrix	= Matrix4()
		self.rotation_matrix= Matrix4()
		self.position_matrix= Matrix4()
		self.scale_matrix	= Matrix4()

		self.result_matrix.set_identity()
		self.rotation_matrix.set_identity()
		self.position_matrix.set_identity()
		self.scale_matrix.set_identity()

		self.need_update	= False
		self.childs			= []
		self.parent			= None

	def getLocalPosition(self):
		return self.position

	def setLocalPosition(self, position):
		self.position = position
		self.position_matrix.setTranslation(position.x,position.y,position.z)

		self.need_update = True

	def setLocalScale(self, scale):
		self.scale = scale
		self.scale_matrix.setScalation(scale.x,scale.y,scale.z)

		self.need_update = True

	def setLocalRotation(self, rotation):
		self.rotation = rotation

		self.rotation_matrix	= self.rotation.to_matrix4()
		self.need_update		= True

	def lookAt(self, direction, up_vector = Vector3(0.0,1.0,0.0) ):
		self.rotation_matrix.setLookMatrix(direction, up_vector)
		self.rotation 			= Quaternion.fromMatrix(self.rotation_matrix)
		self.rotation_matrix 	= self.rotation.toMatrix()

		self.need_update = True

	def getForwardVector(self):
		return self.rotation_matrix.get_z_vector()

	def getUpVector(self):
		return self.rotation_matrix.get_y_vector()

	def getRightVector(self):
		return self.rotation_matrix.get_x_vector()

	def addChild(self, child):
		self.childs.append(child)
		child.parent = self

	def rebuildMatrix(self):
		self.result_matrix	= self.position_matrix * self.rotation_matrix * self.scale_matrix
		self.need_update	= False

		if(self.parent != None):
			self.result_matrix = self.parent.getParentMatrix() * self.result_matrix

		for child in self.childs:
			child.rebuildMatrix()

	def getParentMatrix(self):
		return self.getTransformationMatrix()

	def getTransformationMatrix(self):

		if(self.need_update == True):
			self.rebuildMatrix()
		elif(self.parent != None and self.parent.need_update == True):
			self.rebuildMatrix()

		return self.result_matrix
