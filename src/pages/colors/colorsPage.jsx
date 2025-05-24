import ColorBox from 'src/pages/colors/components/colorBox';

import 'src/styles/shared/colors.css';

import styles from 'src/pages/colors/colorsPage.module.css'


const ColorsPage = () => (
  <div class={styles["colors-page"]}>
    <h2>Colors</h2>
    <p>Colors we're using in our app.</p>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='black1' outline/>
      <ColorBox colorVariable='black2' outline/>
      <ColorBox colorVariable='black3'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='white1'/>
      <ColorBox colorVariable='white2'/>
      <ColorBox colorVariable='white3'/>
      <ColorBox colorVariable='white4'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='violet1'/>
      <ColorBox colorVariable='violet2'/>
      <ColorBox colorVariable='violet3' outline/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='pink1'/>
      <ColorBox colorVariable='pink2'/>
      <ColorBox colorVariable='pink3'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='blue1'/>
      <ColorBox colorVariable='blue2'/>
      <ColorBox colorVariable='blue3'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='green1'/>
      <ColorBox colorVariable='green2'/>
      <ColorBox colorVariable='green3'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='orange1'/>
      <ColorBox colorVariable='orange2'/>
      <ColorBox colorVariable='orange3'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='yellow1'/>
      <ColorBox colorVariable='yellow2'/>
      <ColorBox colorVariable='yellow3'/>
    </div>

    <div class={styles["color-boxes-showcase"]}>
      <ColorBox colorVariable='red1'/>
      <ColorBox colorVariable='red2'/>
      <ColorBox colorVariable='red3'/>
    </div>

  </div>
)


export default ColorsPage;
