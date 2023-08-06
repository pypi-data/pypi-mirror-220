// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

/* list of color names supported in css */
/* https://www.w3schools.com/cssref/css_colors.asp */

const color_hex = {
  "AliceBlue": "#F0F8FF", "AntiqueWhite": "#FAEBD7", "Aqua": "#00FFFF", "Aquamarine": "#7FFFD4", "Azure": "#F0FFFF", "Beige": "#F5F5DC", "Bisque": "#FFE4C4", "Black": "#000000", "BlanchedAlmond": "#FFEBCD", "Blue": "#0000FF", "BlueViolet": "#8A2BE2", "Brown": "#A52A2A", "BurlyWood": "#DEB887", "CadetBlue": "#5F9EA0", "Chartreuse": "#7FFF00", "Chocolate": "#D2691E", "Coral": "#FF7F50", "CornflowerBlue": "#6495ED", "Cornsilk": "#FFF8DC", "Crimson": "#DC143C", "Cyan": "#00FFFF", "DarkBlue": "#00008B", "DarkCyan": "#008B8B", "DarkGoldenRod": "#B8860B", "DarkGray": "#A9A9A9", "DarkGrey": "#A9A9A9", "DarkGreen": "#006400", "DarkKhaki": "#BDB76B", "DarkMagenta": "#8B008B", "DarkOliveGreen": "#556B2F", "DarkOrange": "#FF8C00", "DarkOrchid": "#9932CC", "DarkRed": "#8B0000", "DarkSalmon": "#E9967A", "DarkSeaGreen": "#8FBC8F", "DarkSlateBlue": "#483D8B", "DarkSlateGray": "#2F4F4F", "DarkSlateGrey": "#2F4F4F", "DarkTurquoise": "#00CED1", "DarkViolet": "#9400D3", "DeepPink": "#FF1493", "DeepSkyBlue": "#00BFFF", "DimGray": "#696969", "DimGrey": "#696969", "DodgerBlue": "#1E90FF", "FireBrick": "#B22222", "FloralWhite": "#FFFAF0", "ForestGreen": "#228B22", "Fuchsia": "#FF00FF", "Gainsboro": "#DCDCDC", "GhostWhite": "#F8F8FF", "Gold": "#FFD700", "GoldenRod": "#DAA520", "Gray": "#808080", "Grey": "#808080", "Green": "#008000", "GreenYellow": "#ADFF2F", "HoneyDew": "#F0FFF0", "HotPink": "#FF69B4", "IndianRed": "#CD5C5C", "Indigo": "#4B0082", "Ivory": "#FFFFF0", "Khaki": "#F0E68C", "Lavender": "#E6E6FA", "LavenderBlush": "#FFF0F5", "LawnGreen": "#7CFC00", "LemonChiffon": "#FFFACD", "LightBlue": "#ADD8E6", "LightCoral": "#F08080", "LightCyan": "#E0FFFF", "LightGoldenRodYellow": "#FAFAD2", "LightGray": "#D3D3D3", "LightGrey": "#D3D3D3", "LightGreen": "#90EE90", "LightPink": "#FFB6C1", "LightSalmon": "#FFA07A", "LightSeaGreen": "#20B2AA", "LightSkyBlue": "#87CEFA", "LightSlateGray": "#778899", "LightSlateGrey": "#778899", "LightSteelBlue": "#B0C4DE", "LightYellow": "#FFFFE0", "Lime": "#00FF00", "LimeGreen": "#32CD32", "Linen": "#FAF0E6", "Magenta": "#FF00FF", "Maroon": "#800000", "MediumAquaMarine": "#66CDAA", "MediumBlue": "#0000CD", "MediumOrchid": "#BA55D3", "MediumPurple": "#9370DB", "MediumSeaGreen": "#3CB371", "MediumSlateBlue": "#7B68EE", "MediumSpringGreen": "#00FA9A", "MediumTurquoise": "#48D1CC", "MediumVioletRed": "#C71585", "MidnightBlue": "#191970", "MintCream": "#F5FFFA", "MistyRose": "#FFE4E1", "Moccasin": "#FFE4B5", "NavajoWhite": "#FFDEAD", "Navy": "#000080", "OldLace": "#FDF5E6", "Olive": "#808000", "OliveDrab": "#6B8E23", "Orange": "#FFA500", "OrangeRed": "#FF4500", "Orchid": "#DA70D6", "PaleGoldenRod": "#EEE8AA", "PaleGreen": "#98FB98", "PaleTurquoise": "#AFEEEE", "PaleVioletRed": "#DB7093", "PapayaWhip": "#FFEFD5", "PeachPuff": "#FFDAB9", "Peru": "#CD853F", "Pink": "#FFC0CB", "Plum": "#DDA0DD", "PowderBlue": "#B0E0E6", "Purple": "#800080", "RebeccaPurple": "#663399", "Red": "#FF0000", "RosyBrown": "#BC8F8F", "RoyalBlue": "#4169E1", "SaddleBrown": "#8B4513", "Salmon": "#FA8072", "SandyBrown": "#F4A460", "SeaGreen": "#2E8B57", "SeaShell": "#FFF5EE", "Sienna": "#A0522D", "Silver": "#C0C0C0", "SkyBlue": "#87CEEB", "SlateBlue": "#6A5ACD", "SlateGray": "#708090", "SlateGrey": "#708090", "Snow": "#FFFAFA", "SpringGreen": "#00FF7F", "SteelBlue": "#4682B4", "Tan": "#D2B48C", "Teal": "#008080", "Thistle": "#D8BFD8", "Tomato": "#FF6347", "Turquoise": "#40E0D0", "Violet": "#EE82EE", "Wheat": "#F5DEB3", "White": "#FFFFFF", "WhiteSmoke": "#F5F5F5", "Yellow": "#FFFF00", "YellowGreen": "#9ACD32"
}

const colors = Object.values(color_hex);

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

function getContrastColor(hexcolor){
  hexcolor = hexcolor.replace("#", "");
  var r = parseInt(hexcolor.substr(0,2),16);
  var g = parseInt(hexcolor.substr(2,2),16);
  var b = parseInt(hexcolor.substr(4,2),16);
  var yiq = ((r*299)+(g*587)+(b*114))/1000;
  return (yiq >= 128) ? 'black' : 'white';
}

function highlightSelection() {
  var selection = window.getSelection();
  // if nothing is selected, return empty string
  if (!selection.toString()) {
    return {
      selected: "",
      value: "",
      color: ""
    }
  }
  if (selection.rangeCount) {
      var range = selection.getRangeAt(0);
      var newNode = document.createElement("span");
      // count </span> in the innerHTML to get the index of the color
      let color_index = 0;
      if (document.getElementById("root").innerHTML.match(/<\/span>/g)) {
        color_index = document.getElementById("root").innerHTML.match(/<\/span>/g).length;
      }
      const color = colors[color_index % colors.length]
      const text_color = getContrastColor(color);
      newNode.setAttribute('style', `background-color: ${color}; color: ${text_color}`);
      newNode.appendChild(range.extractContents());
      range.insertNode(newNode);
      return {
        selected: newNode.innerHTML ? newNode.innerHTML : "",
        value: document.getElementById("root").innerHTML,
        color: color,
        contrast: text_color
      }
  }
  return {
    selected: "",
    value: "",
    color: "",
  }
}

const getSelectionText = () => {
  let selectedText = highlightSelection();
  // window.getSelection()?.toString();
  if (selectedText.selected.length > 0) {
    sendValue(selectedText)
  }
};

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    // You most likely want to get the data passed in like this
    const {value} = event.detail.args
    // get div with id root and set innerHTML to value
    document.getElementById("root").innerHTML = value;
    // You'll most likely want to pass some data back to Python like this
    document.onmouseup = document.onkeyup = getSelectionText;
    // sendValue({selected: "foo", output2: "bar"})
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Render with the correct height, if this is a fixed-height component
Streamlit.setFrameHeight(400)
