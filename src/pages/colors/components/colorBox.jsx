import 'src/pages/colors/components/colorBox.css';

const ColorBox = (props) => {
  const color = `--${props.colorVariable}`

  let style = `background-color: var(${color});`;
  if (props.outline) {
    style += "outline: 1px dashed grey";
  }

  return (
    <div class='color-box'>
      <div class="color" style={style}></div>
      <div class='hint'>{color}</div>
    </div>
  )
}


export default ColorBox;
