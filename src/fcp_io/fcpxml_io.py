import xml.etree.ElementTree as ET
import os
import shutil

def get_fcpxml(filepath):
    """
    returns tree, root (XML)
    """
    # structure filepath
    filepath = os.path.abspath(filepath)
    d, b = os.path.split(filepath)
    fcpxml_filename = 'Info.fcpxml'
    filepath = os.path.join(filepath, fcpxml_filename)

    # get the relevant xml tree from FCPXML
    tree = ET.parse(filepath)
    root = tree.getroot()

    return tree, root

def get_resources(root):
    parent = root
    return parent.find('resources')

def get_format(root):
    parent = get_resources(root)
    return parent.find('format')

def get_fps(root):
    parent = get_format(root)
    return parent.get('frameDuration')

def get_spine(root):
    """
    Returns the spine element of xml.
    """
    return root.find(".//spine")

#def get_asset_clip(root):
def get_last_asset_clip(spine):
    """
    Assumption: root contains only one asset and only one asset-clip in the spine of the Project Timeline.
    Returns the last occurrence of spine asset-clip that the cell division task will be done.
    """
    clips = spine.findall('asset-clip')
    return clips[-1]

#def save(tree, src_filepath, affix=''):
def save_with_affix(tree, src_filepath, affix=''):
    """
    Stores the worked fcpxml in the same folder as the source filepath with the affix attached to the new file name.
    """
    # Save the new FCPXML file
    #filepath = os.path.abspath(filepath)
    #d, b = os.path.split(filepath)
    fcpxml_filename = 'Info.fcpxml'
    #filepath = os.path.join(filepath, fcpxml_filename)

    #src_filepath = os.path.join(d, b) # still *.fcpxmld folder path
    d, b = os.path.split(src_filepath)
    new_filepath = os.path.join(d, affix+b) # silence_marked_*.fcpxmld a new foler path
    shutil.copytree(src_filepath, new_filepath, dirs_exist_ok=True) # create the new folder
    destination_filepath = os.path.join(new_filepath, fcpxml_filename) # *.fcpxml file
    ET.indent(tree, space="\t", level=0)
    tree.write(destination_filepath, encoding='UTF-8', xml_declaration=True)

