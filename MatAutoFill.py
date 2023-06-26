import maya.cmds as cmds
import maya.mel as mel


def createMaterial(*args):
    textures = opendialog()
    makeTemplate(textures)


def makeTemplate(textures):

    ai_name = cmds.shadingNode('aiStandardSurface', asShader=True)
    sgname = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)
    cmds.connectAttr(ai_name + '.outColor', sgname + '.surfaceShader', f=True)

    if cmds.checkBox(checkBox1, query=True, value=True):
        for texture in [basename, roughname, metalname, normalname, eminame, disname]:
            cmds.setAttr(texture + '.uvTilingMode', 3)
            mel.eval('generateUvTilePreview ' + texture)

    for i in range(len(textures)):
        print(textures[i])
        if 'Base' in textures[i] or 'base' in textures[i]:
            basename = fileNode()
            p2dname1 = p2dNode()
            cmds.setAttr(basename + '.fileTextureName', textures[i],type="string")
            cmds.connectAttr(basename + '.outColor', ai_name + '.baseColor', f=True)
            cmds.connectAttr(p2dname1 + '.outUV', basename + '.uvCoord', f=True)

        elif 'Roughness' in textures[i] or 'roughness' in textures[i]:
            roughname = fileNode()
            p2dname2 = p2dNode()
            cmds.setAttr(roughname + '.fileTextureName', textures[i],type="string")
            cmds.setAttr(roughname + '.colorSpace', "Raw",type="string")
            cmds.connectAttr(roughname + '.outAlpha', ai_name + '.specularRoughness', f=True)
            cmds.connectAttr(p2dname2 + '.outUV', roughname + '.uvCoord', f=True)

        elif 'Metallic' in textures[i] or 'Metalness' in textures[i] or 'metallic' in textures[i]:
            metalname = fileNode()
            p2dname3 = p2dNode()
            cmds.setAttr(metalname + '.fileTextureName', textures[i],type="string")
            cmds.setAttr(metalname + '.colorSpace', "Raw",type="string")
            cmds.connectAttr(metalname + '.outAlpha', ai_name + '.metalness', f=True)
            cmds.connectAttr(p2dname3 + '.outUV', metalname + '.uvCoord', f=True)

        elif 'Normal' in textures[i] or 'Normal_OpenGL' in textures[i] or 'normal' in textures[i] or 'Norm' in textures[i]:
            normalname = fileNode()
            p2dname4 = p2dNode()
            bname = cmds.shadingNode('bump2d', asUtility=True)
            aibname = cmds.shadingNode('aiNormalMap', asUtility=True)
            cmds.setAttr(bname + '.bumpInterp',1)
            cmds.setAttr(normalname + '.fileTextureName',textures[i],type="string")
            cmds.setAttr(normalname + '.colorSpace',"Raw",type="string")
            cmds.connectAttr(normalname + '.outColor', aibname + '.input', f=True)
            cmds.connectAttr(p2dname4 + '.outUV', normalname + '.uvCoord', f=True)
            cmds.connectAttr(aibname + '.outValue', ai_name + '.normalCamera', f=True)

        elif 'Emissive' in textures[i]:
            eminame = fileNode()
            p2dname5 = p2dNode()
            cmds.setAttr(eminame + '.fileTextureName',textures[i],type="string")
            cmds.connectAttr(eminame + '.outAlpha', ai_name + '.emission', f=True)
            cmds.connectAttr(p2dname5 + '.outUV', eminame + '.uvCoord', f=True)

        elif 'Height' in textures[i] or 'height' in textures[i]:
            disname = fileNode()
            disshader = cmds.shadingNode('displacementShader', asShader=True)
            p2dname6 = p2dNode()
            cmds.setAttr(disname + '.fileTextureName',textures[i],type="string")
            cmds.setAttr(disshader + '.scale',0.1)
            cmds.connectAttr(p2dname6 + '.outUV', disname + '.uvCoord', f=True)
            cmds.connectAttr(disname + '.outAlpha', disshader + '.displacement', f=True)
            cmds.connectAttr(disshader + '.displacement', sgname + '.displacementShader', f=True)


def fileNode():
    return cmds.shadingNode('file', asTexture=True, isColorManaged=True)

def p2dNode():
    return cmds.shadingNode('place2dTexture', asUtility=True)

def opendialog():
    textures = cmds.fileDialog2(fileMode=4, caption="Connect Image")
    if not textures:
        print("No texture file selected.")
    else:
        return textures

checkBox1 = cmds.checkBox(label='UDIM Activation')

cmds.window(title='autofilenode')
cmds.columnLayout(adjustableColumn=True)
cmds.frameLayout(label='AutoFileNode(SubStance Texture Multiple Shader Auto Generation)', labelAlign='top')
cmds.button(label='Select File (Base_Color, Roughness, Metallic, Normal, Emission, Height)', command=createMaterial)
cmds.showWindow()
