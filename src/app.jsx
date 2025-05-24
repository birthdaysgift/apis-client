import Router from 'preact-router';

import HomePage from 'src/pages/home/homePage';
import ComponentsPage from 'src/pages/components/componentsPage';
import ColorsPage from 'src/pages/colors/colorsPage';
import FontsPage from 'src/pages/fonts/fontsPage';
import LayoutsPage from 'src/pages/layouts/layoutsPage';

import styles from "src/app.module.css"


export function App() {
  return (
    <div class={styles["app"]}>
      <Router>
        <HomePage path="/" />
        <ColorsPage path="/colors" />
        <ComponentsPage path="/components" />
        <FontsPage path="/fonts" />
        <LayoutsPage path="/layouts" />
      </Router>
    </div>
  )
}
