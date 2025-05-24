import Router from 'preact-router';

import HomePage from './pages/home/homePage';
import ComponentsPage from './pages/components/componentsPage';
import ColorsPage from './pages/colors/colorsPage';
import FontsPage from './pages/fonts/fontsPage';
import LayoutsPage from './pages/layouts/layoutsPage';

import styles from "./app.module.css"


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
