import { FC, useEffect } from 'react';
import { useDispatch, useSelector } from '../../utils/type/store';
import style from './Header.module.css';
import burger from '../../images/burger_menu.svg';
import logoYandex from '../../images/logo_yandex.svg';
import logoYandexMarket from '../../images/logo_yandex-market.svg';
import rocket from '../../images/icon_rocket.svg';
import actionMenu from '../../images/icon_action-menu.svg';
import { getUser } from '../../services/actions/userActions';
import { setCookie } from '../../utils/cookie';

const Header: FC = () => {
  const user = useSelector(store => store.userInfo.user);
  const userInfo = useSelector(store => store.userInfo);
  const dispatch = useDispatch();

  useEffect(() => {
    dispatch(getUser())
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [])

  // userInfo.error && setCookie('token', '');

  return (
    <header className={style.header}>
      <div className={style.wrapper}>
        <button className={style.btnBurger}>
          <img src={burger} alt="Кнопка бургер меню" />
        </button>
        <div className={style.logos}>
          <a href='https://ya.ru/' className={style.link} target="_blank" rel="noopener noreferrer">
            <img className={style.logo} src={logoYandex} alt="Логотип Яндекс" />
          </a>
          <a href='https://market.yandex.ru/' className={style.link} target="_blank" rel="noopener noreferrer">
            <img className={style.logo} src={logoYandexMarket} alt="Логотип Яндекс Маркета" />
          </a>
        </div>
        <h1 className={style.title}>Склад</h1>
      </div>
      <div className={style.wrapperStat}>
        <div className={style.statistics}>
          <span className={style.nickname}>{user.username}</span>
          <div className={style.buttons}>
            <button className={style.btnKpi}>KPI</button>
            <button className={style.btnStat}>
              <img src={rocket} alt="Рокета" />
              <span className={style.statUser}>97%</span>
            </button>
          </div>
        </div>
        <button className={style.btnActionMenu}>
          <img src={actionMenu} alt="Кнопка Меню" />
        </button>
      </div>
    </header>
  )
}

export default Header;
