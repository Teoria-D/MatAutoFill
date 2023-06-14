#21au0138 Toma Wake
#MatAutofill
#Substanceなど、特定の命名規則が割り当てられたテクスチャを選択するだけでシェーダーを作成できるツールです
import pymel.core as pm
import maya.cmds as mc
import maya.mel as mel

def maketemplate(thedialog):
    
    ainame = pm.shadingNode('aiStandardSurface', asShader=True)
    sgname = pm.sets(renderable=True, noSurfaceShader=True, empty=True)
    pm.connectAttr(ainame + '.outColor', sgname + '.surfaceShader', f=True)
    
    if checkBox1.getValue():
        pm.setAttr(basename + '.uvTilingMode',3)
        mel.eval('generateUvTilePreview '+basename)
        pm.setAttr(roughname + '.uvTilingMode',3)
        mel.eval('generateUvTilePreview '+roughname)
        pm.setAttr(metalname + '.uvTilingMode',3)
        mel.eval('generateUvTilePreview '+metalname)
        pm.setAttr(normalname + '.uvTilingMode',3)
        mel.eval('generateUvTilePreview '+normalname)
        pm.setAttr(eminame + '.uvTilingMode',3)
        mel.eval('generateUvTilePreview '+eminame)
        pm.setAttr(disname + '.uvTilingMode',3)
        mel.eval('generateUvTilePreview '+disname)
    
        
    for i in range(len(thedialog)):
        if('Base_color' in thedialog[i] or 'BaseColor' in thedialog[i] or 'Base Color' in thedialog[i]):
            basename = pm.shadingNode('file', asTexture=True, isColorManaged=True)
            p2dname1 = pm.shadingNode('place2dTexture', asUtility=True)
            pm.setAttr(basename + '.fileTextureName',thedialog[i])
            pm.connectAttr(basename + '.outColor', ainame + '.baseColor', f=True)
            pm.connectAttr(p2dname1 + '.outUV', basename + '.uvCoord', f=True)
        elif('Roughness' in thedialog[i] or 'roughness' in thedialog[i]):
            roughname = pm.shadingNode('file', asTexture=True, isColorManaged=True)
            p2dname2 = pm.shadingNode('place2dTexture', asUtility=True)
            pm.setAttr(roughname + '.fileTextureName',thedialog[i])
            pm.setAttr(roughname + '.colorSpace',"Raw")
            pm.connectAttr(roughname + '.outAlpha', ainame + '.specularRoughness', f=True)
            pm.connectAttr(p2dname2 + '.outUV', roughname + '.uvCoord', f=True)
        elif('Metallic' in thedialog[i] or 'Metalness' in thedialog[i] or 'metallic' in thedialog[i]):
            metalname = pm.shadingNode('file', asTexture=True, isColorManaged=True)
            p2dname3 = pm.shadingNode('place2dTexture', asUtility=True)
            pm.setAttr(metalname + '.fileTextureName',thedialog[i])
            pm.setAttr(metalname + '.colorSpace',"Raw")
            pm.connectAttr(metalname + '.outAlpha', ainame + '.metalness', f=True)
            pm.connectAttr(p2dname3 + '.outUV', metalname + '.uvCoord', f=True)
        elif('Normal' in thedialog[i] or 'Normal_OpenGL' in thedialog[i] or 'normal' in thedialog[i] or 'Norm' in thedialog[i]):
            normalname = pm.shadingNode('file', asTexture=True, isColorManaged=True)
            p2dname4 = pm.shadingNode('place2dTexture', asUtility=True)
            bname = pm.shadingNode('bump2d', asUtility=True)
            aibname = pm.shadingNode('aiNormalMap', asUtility=True)
            pm.setAttr(bname + '.bumpInterp',1)
            pm.setAttr(normalname + '.fileTextureName',thedialog[i])
            pm.setAttr(normalname + '.colorSpace',"Raw")
            pm.connectAttr(normalname + '.outColor', aibname + '.input', f=True)
            pm.connectAttr(p2dname4 + '.outUV', normalname + '.uvCoord', f=True)
            pm.connectAttr(aibname + '.outValue', ainame + '.normalCamera', f=True)
        elif('Emissive' in thedialog[i]):
            eminame = pm.shadingNode('file', asTexture=True, isColorManaged=True)
            p2dname5 = pm.shadingNode('place2dTexture', asUtility=True)
            pm.setAttr(eminame + '.fileTextureName',thedialog[i])
            pm.connectAttr(eminame + '.outAlpha', ainame + '.emission', f=True)
            pm.connectAttr(p2dname5 + '.outUV', eminame + '.uvCoord', f=True)
        elif('Height' in thedialog[i]):
            disname = pm.shadingNode('file', asTexture=True, isColorManaged=True)
            disshader = pm.shadingNode('displacementShader', asShader=True)
            p2dname6 = pm.shadingNode('place2dTexture', asUtility=True)
            pm.setAttr(disname + '.fileTextureName',thedialog[i])
            pm.setAttr(disshader + '.scale',0.1)
            pm.connectAttr(p2dname6 + '.outUV', disname + '.uvCoord', f=True)
            pm.connectAttr(disname + '.outAlpha', disshader + '.displacement', f=True)
            pm.connectAttr(disshader + '.displacement', sgname + '.displacementShader', f=True)
            
    
    
def opendialog():
    thedialog = pm.fileDialog2(fileMode=4, caption="Connect Image")
    if not thedialog:
        print("No texture file selected.")
    else:
        maketemplate(thedialog) 
    
    

with pm.window(title='autofilenode',width=300,height=50):
    with pm.horizontalLayout():
        pm.frameLayout(label='AutoFileNode(SubStanceのテクスチャ複数からシェーダーを自動生成します。',labelAlign='top');
        pm.button(label='ファイル選択(Base_Color,Roughness,Metallic,Normal,Emission,Height)',command='opendialog()')
        checkBox1 = pm.checkBox(label=u'UDIM有効化')
