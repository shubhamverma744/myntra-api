import './Footer.jsx';

function Footer() {
  return (
    <footer className="myntra-footer">
      <div className="footer-section">
        <h4>ONLINE SHOPPING</h4>
        <ul>
          <li>
            <a href="#">Men</a>
          </li>
          <li>
            <a href="#">Women</a>
          </li>
          <li>
            <a href="#">Kids</a>
          </li>
          <li>
            <a href="#">Home</a>
          </li>
          <li>
            <a href="#">Beauty</a>
          </li>
        </ul>
      </div>

      <div className="footer-section">
        <h4>CUSTOMER POLICIES</h4>
        <ul>
          <li>
            <a href="#">Contact Us</a>
          </li>

          <li>
            <a href="#">T&C</a>
          </li>
          <li>
            <a href="#">Terms of Use</a>
          </li>
          <li>
            <a href="#">Track Orders</a>
          </li>
        </ul>
      </div>

      <div className="footer-section">
        <h4>EXPERIENCE MYNTRA APP</h4>
        <li>
          <a href="https://play.google.com/store/apps/details?id=com.myntra.android&pcampaignid=web_share">
            GOOGLE PLAY{' '}
          </a>
        </li>
        <li>
          <a href="https://apps.apple.com/in/app/myntra-fashion-shopping-app/id907394059">
            APP STORE
          </a>
        </li>
      </div>

      <div className="footer-bottom">
        <p>www.myntra.com. ©All rights reserved.</p>
      </div>
    </footer>
  );
}

export default Footer;
