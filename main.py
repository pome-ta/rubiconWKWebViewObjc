from pathlib import Path

from pyrubicon.objc.api import ObjCClass, ObjCProtocol, objc_method, objc_property
from pyrubicon.objc.runtime import SEL, send_super, load_library, objc_id
from pyrubicon.objc.types import CGRect

from rbedge.enumerations import (
  NSURLRequestCachePolicy,
  UIControlEvents,
)
from rbedge.functions import NSStringFromClass

UIViewController = ObjCClass('UIViewController')
UIColor = ObjCClass('UIColor')
NSLayoutConstraint = ObjCClass('NSLayoutConstraint')
CoreGraphics = load_library('CoreGraphics')
CGRectZero = CGRect.in_dll(CoreGraphics, 'CGRectZero')

NSURL = ObjCClass('NSURL')
NSURLRequest = ObjCClass('NSURLRequest')

# --- WKWebView
WKWebView = ObjCClass('WKWebView')
WKWebViewConfiguration = ObjCClass('WKWebViewConfiguration')
WKWebsiteDataStore = ObjCClass('WKWebsiteDataStore')

UIRefreshControl = ObjCClass('UIRefreshControl')

WKUIDelegate = ObjCProtocol('WKUIDelegate')
WKNavigationDelegate = ObjCProtocol('WKNavigationDelegate')


class WebViewController(UIViewController,
                        protocols=[
                          WKUIDelegate,
                          WKNavigationDelegate,
                        ]):

  webView: WKWebView = objc_property()
  targetURL: Path | str = Path('./src/index.html')

  @objc_method
  def loadView(self):
    send_super(__class__, self, 'loadView')
    webConfiguration = WKWebViewConfiguration.new()
    websiteDataStore = WKWebsiteDataStore.nonPersistentDataStore()

    webConfiguration.websiteDataStore = websiteDataStore
    webConfiguration.preferences.setValue_forKey_(
      True, 'allowFileAccessFromFileURLs')

    self.webView = WKWebView.alloc().initWithFrame_configuration_(
      CGRectZero, webConfiguration)
    #self.webView.uiDelegate = self
    self.webView.navigationDelegate = self

    self.webView.scrollView.bounces = True

    refreshControl = UIRefreshControl.new()
    refreshControl.addTarget_action_forControlEvents_(
      self, SEL('refreshWebView:'), UIControlEvents.valueChanged)

    self.webView.scrollView.refreshControl = refreshControl
    self.view = self.webView
    #pdbr.state(self.webView)

  @objc_method
  def viewDidLoad(self):
    send_super(__class__, self, 'viewDidLoad')  # xxx: 不要?
    title = NSStringFromClass(__class__)
    self.navigationItem.title = title
    self.view.backgroundColor = UIColor.systemDarkRedColor()

    # --- load url
    if (Path(self.targetURL).exists()):
      target_path = Path(self.targetURL)
      fileURLWithPath = NSURL.fileURLWithPath_isDirectory_
      folder_path = fileURLWithPath(str(target_path.parent), True)
      index_path = fileURLWithPath(str(target_path), False)
      self.webView.loadFileURL_allowingReadAccessToURL_(
        index_path, folder_path)
    else:
      url = NSURL.URLWithString_(self.targetURL)
      cachePolicy = NSURLRequestCachePolicy.reloadIgnoringLocalCacheData
      timeoutInterval = 10
      request = NSURLRequest.requestWithURL_cachePolicy_timeoutInterval_(
        url, cachePolicy, timeoutInterval)

      self.webView.loadRequest_(request)

  @objc_method
  def refreshWebView_(self, sender):
    self.webView.reload()
    sender.endRefreshing()

  # --- WKNavigationDelegate
  @objc_method
  def webView_didCommitNavigation_(self, webView, navigation):
    # 遷移開始時
    #print('didCommitNavigation')
    pass

  @objc_method
  def webView_didFailNavigation_withError_(self, webView, navigation, error):
    # 遷移中にエラーが発生した時
    # xxx: 未確認
    print('didFailNavigation_withError')
    print(error)

  @objc_method
  def webView_didFailProvisionalNavigation_withError_(self, webView,
                                                      navigation, error):
    # ページ読み込み時にエラーが発生した時
    print('didFailProvisionalNavigation_withError')
    print(error)

  @objc_method
  def webView_didFinishNavigation_(self, webView, navigation):
    # ページ読み込みが完了した時
    #print('didFinishNavigation')
    title = webView.title
    self.navigationItem.title = str(title)

  '''
  @objc_method
  def webView_didReceiveAuthenticationChallenge_completionHandler_(
      self, webView, challenge, completionHandler):
    # 認証が必要な時
    # xxx: 未確認
    print('didReceiveAuthenticationChallenge_completionHandler')
    print(completionHandler)
  '''

  @objc_method
  def webView_didReceiveServerRedirectForProvisionalNavigation_(
      self, webView, navigation):
    # リダイレクトされた時
    # xxx: 未確認
    print('didReceiveServerRedirectForProvisionalNavigation')

  @objc_method
  def webView_didStartProvisionalNavigation_(self, webView, navigation):
    # ページ読み込みが開始された時
    #print('didStartProvisionalNavigation')
    pass


if __name__ == '__main__':
  from rbedge.enumerations import UIModalPresentationStyle
  from rbedge.app import App
  from rbedge import pdbr

  target_url = Path('./src/index.html')
  #target_url = 'https://www.apple.com'

  main_vc = WebViewController.new()
  main_vc.targetURL = target_url
  app = App(main_vc)

  presentation_style = UIModalPresentationStyle.fullScreen
  app.main_loop(presentation_style)

