import ColorBox from 'src/pages/colors/components/colorBox';
import 'src/pages/colors/colorsPage.css';

import 'src/styles/shared/colors.css';


const ColorsPage = () => (
  <div class='colors-page bg-primary text-color-primary'>
    <h2>Colors</h2>
    <p>Colors we're using for our app.</p>
    <div id='color-boxes-showcase'>
      <ColorBox colorVariable='green-color'/>
      <ColorBox colorVariable='blue-color'/>
      <ColorBox colorVariable='red-color'/>
      <ColorBox colorVariable='bg-primary' outline={true}/>
    </div>
  </div>
)


export default ColorsPage;
