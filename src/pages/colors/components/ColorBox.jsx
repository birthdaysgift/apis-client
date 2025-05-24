import styles from 'src/pages/colors/components/ColorBox.module.css';

const ColorBox = (props) => {
  const color = `--${props.colorVariable}`

  let style = `background-color: var(${color});`;
  if (props.outline) {
    style += "outline: 1px dashed grey";
  }

  return (
    <div class={styles["color-box"]}>
      <div class={styles["color"]} style={style}></div>
      <div class={styles["hint"]}>{color}</div>
    </div>
  )
}


export default ColorBox;
