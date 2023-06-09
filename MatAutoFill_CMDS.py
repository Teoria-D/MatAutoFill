import maya.cmds as cmds
import maya.mel as mel


def maketemplate(thedialog):
    ainame = cmds.shadingNode('aiStandardSurface', asShader=True)

    basename = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    roughname = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    metalname = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    normalname = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    eminame = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    disname = cmds.shadingNode('file', asTexture=True, isColorManaged=True)
    disshader = cmds.shadingNode('displacementShader', asShader=True)

    p2dname1 = cmds.shadingNode('place2dTexture', asUtility=True)
    p2dname2 = cmds.shadingNode('place2dTexture', asUtility=True)
    p2dname3 = cmds.shadingNode('place2dTexture', asUtility=True)
    p2dname4 = cmds.shadingNode('place2dTexture', asUtility=True)
    p2dname5 = cmds.shadingNode('place2dTexture', asUtility=True)
    p2dname6 = cmds.shadingNode('place2dTexture', asUtility=True)

    bname = cmds.shadingNode('bump2d', asUtility=True)
    aibname = cmds.shadingNode('aiNormalMap', asUtility=True)
    cmds.setAttr(bname + '.bumpInterp', 1)

    sgname = cmds.sets(renderable=True, noSurfaceShader=True, empty=True)

    cmds.connectAttr(ainame + '.outColor', sgname + '.surfaceShader', f=True)

    if cmds.checkBox(checkBox1, q=True, v=True):
        cmds.setAttr(basename + '.uvTilingMode', 3)
        mel.eval('generateUvTilePreview ' + basename)
        cmds.setAttr(roughname + '.uvTilingMode', 3)
        mel.eval('generateUvTilePreview ' + roughname)
        cmds.setAttr(metalname + '.uvTilingMode', 3)
        mel.eval('generateUvTilePreview ' + metalname)
        cmds.setAttr(normalname + '.uvTilingMode', 3)
        mel.eval('generateUvTilePreview ' + normalname)
        cmds.setAttr(eminame + '.uvTilingMode', 3)
        mel.eval('generateUvTilePreview ' + eminame)
        cmds.setAttr(disname + '.uvTilingMode', 3)
        mel.eval('generateUvTilePreview ' + disname)

    for item in thedialog:
        if 'Base_color' in item or 'BaseColor' in item or 'Base Color' in item:
            cmds.setAttr(basename + '.fileTextureName', item)
            cmds.connectAttr(basename + '.outColor', ainame + '.baseColor', f=True)
            cmds.connectAttr(p2dname1 + '.outUV', basename + '.uvCoord', f=True)
        elif 'Roughness' in item:
            cmds.setAttr(roughname + '.fileTextureName', item)
            cmds.setAttr(roughname + '.colorSpace', "Raw")
            cmds.connectAttr(roughname + '.outAlpha', ainame +'.specularRoughness', f=True)
            cmds.connectAttr(p2dname2 + '.outUV', roughname + '.uvCoord', f=True)
        elif 'Metallic' in item or 'Metalness' in item:
            cmds.setAttr(metalname + '.fileTextureName', item)
            cmds.setAttr(metalname + '.colorSpace', "Raw")
            cmds.connectAttr(metalname + '.outAlpha', ainame + '.metalness', f=True)
            cmds.connectAttr(p2dname3 + '.outUV', metalname + '.uvCoord', f=True)
        elif 'Normal' in item or 'Normal_OpenGL' in item or 'normal' in item or 'Norm' in item:
            cmds.setAttr(normalname + '.fileTextureName', item)
            cmds.setAttr(normalname + '.colorSpace', "Raw")
            cmds.connectAttr(normalname + '.outColor', aibname + '.input', f=True)
            cmds.connectAttr(p2dname4 + '.outUV', normalname + '.uvCoord', f=True)
            cmds.connectAttr(aibname + '.outValue', ainame + '.normalCamera', f=True)
        elif 'Emissive' in item:
            cmds.setAttr(eminame + '.fileTextureName', item)
            cmds.connectAttr(eminame + '.outAlpha', ainame + '.emission', f=True)
            cmds.connectAttr(p2dname5 + '.outUV', eminame + '.uvCoord', f=True)
        elif 'Height' in item:
            cmds.setAttr(disname + '.fileTextureName', item)
            cmds.setAttr(disshader + '.scale', 0.1)
            cmds.connectAttr(p2dname6 + '.outUV', disname + '.uvCoord', f=True)
            cmds.connectAttr(disname + '.outAlpha', disshader + '.displacement', f=True)
            cmds.connectAttr(disshader + '.displacement', sgname + '.displacementShader', f=True)

def opendialog():
    thedialog = cmds.fileDialog2(fileMode=4, caption="Connect Image")
    maketemplate(thedialog)

window = cmds.window(title='autofilenode', widthHeight=(300, 50))

cmds.frameLayout(label='AutoFileNode(SubStanceのテクスチャ複数からシェーダーを自動生成します。', labelAlign='top', borderStyle='in')
cmds.button(label='ファイル選択(Base_Color,Roughness,Metallic,Normal,Emission,Height)', command='opendialog()')
checkBox1 = cmds.checkBox(label=u'UDIM有効化')

cmds.setParent()
cmds.showWindow(window)
