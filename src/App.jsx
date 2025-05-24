import Router from 'preact-router';

import HomePage from 'src/pages/home/HomePage';
import ComponentsPage from 'src/pages/components/ComponentsPage';
import ColorsPage from 'src/pages/colors/ColorsPage';
import FontsPage from 'src/pages/fonts/FontsPage';
import LayoutsPage from 'src/pages/layouts/LayoutsPage';

import styles from "src/App.module.css"


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
