from panda3d.core import PandaNode, Loader, NodePath, CollisionNode, CollisionSphere, CollisionInvSphere, CollisionCapsule, Vec3

class PlacedObject(PandaNode):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):

        self.modelNode = loader.loadModel(modelPath)

        if not isinstance(self.modelNode, NodePath):
            raise AssertionError("PlacedObject loader.loadModel( " + modelPath + ") did not return a proper PandaNode")

        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)

class CollideableObject(PlacedObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str):
        super(CollideableObject, self).__init__(loader, modelPath, parentNode, nodeName)

        self.collisionNode = self.modelNode.attachNewNode(CollisionNode(nodeName + '_cNode'))
        self.collisionNode.show()

class InverseSphereCollideObject(CollideableObject):
    def __init__(self, loader, modelPath, parentNode, nodeName, colPositionVec, colRadius):
        super(InverseSphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)

        self.collisionNode.node().addSolid(CollisionInvSphere(colPositionVec, colRadius))
        self.collisionNode.show()

class SphereCollideObject(CollideableObject):
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
                 texPath: str, posVec: Vec3, scale: float,
                 colPosVec: Vec3 = Vec3(0, 0, 0), colRadius: float = 1.0) -> None:
        super(SphereCollideObject, self).__init__(loader, modelPath, parentNode, nodeName)

        self.collisionNode.node().addSolid(CollisionSphere(colPosVec, colRadius))
        self.collisionNode.show()

        tex = loader.loadTexture(texPath)
        self.modelNode.setTexture(tex, 1)
        self.modelNode.setPos(posVec)
        self.modelNode.setScale(scale)

class CapsuleCollideObject:
    def __init__(self, loader: Loader, modelPath: str, parentNode: NodePath, nodeName: str,
                 ax: float, ay: float, az: float, bx: float, by: float, bz: float, r: float):
        self.modelNode = loader.loadModel(modelPath)
        self.modelNode.reparentTo(parentNode)
        self.modelNode.setName(nodeName)
        capsule = CollisionCapsule(ax, ay, az, bx, by, bz, r)
        self.collisionNode = CollisionNode(nodeName + '_cNode')
        self.collisionNode.addSolid(capsule)
        self.collisionNodePath = self.modelNode.attachNewNode(self.collisionNode)
        self.collisionNodePath.show()