# oneHTTP simple HTTP request management
import requests
import pickle
from bs4 import BeautifulSoup
from copy import deepcopy
from urllib.parse import urlparse
import os
import hashlib
from datetime import datetime
import pdfkit

class httpSession:
    HISTORY_CONTENT = {}
    HISTORY = []
    HEADERS = {'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"}

    def __init__(self, recordHistory=False, cookies=False) -> None:
        self.request = requests.Session()
        self.last_request = None
        self.recordHistory = False
        self.loadCookies()
        if recordHistory:
            self.mkDir("History")
            self.recordHistory = True

    def get(self, *args, **kwargs):
        self.last_request = self.request.get(*args, **kwargs)
        if self.recordHistory:
            self.registerHistory(self.last_request)

    def post(self, *args, **kwargs):
        self.last_request = self.request.post(*args, **kwargs)
        if self.recordHistory:
            self.registerHistory(self.last_request)
    
    def put(self, *args, **kwargs):
        self.last_request = self.request.put(*args, **kwargs)
        if self.recordHistory:
            self.registerHistory(self.last_request)

    def patch(self, *args, **kwargs):
        self.last_request = self.request.patch(*args, **kwargs)
        if self.recordHistory:
            self.registerHistory(self.last_request)

    def delete(self, *args, **kwargs):
        self.last_request = self.request.delete(*args, **kwargs)
        if self.recordHistory:
            self.registerHistory(self.last_request)

    def head(self, *args, **kwargs):
        self.last_request = self.request.head(*args, **kwargs)
        if self.recordHistory:
            self.registerHistory(self.last_request)

    def savePage(self, save_name, scantags=['link:href', 'script:src', 'a:href', 'img:src']):
        page_dir = save_name
        page_files = page_dir + '/' + 'page_files'
        try:
            os.mkdir(page_dir)
        except Exception:
            pass
        try:
            os.mkdir(page_files)
        except Exception:
            pass
        content = self.last_request.content
        current_url = self.last_request.url
        soup = BeautifulSoup(content, features="html.parser")
        for eachTag in scantags:
            attribute_ = eachTag.split(':')[1]
            tag = eachTag.split(':')[0]
            results = soup.find_all(tag)
            for eachLink in results:
                link = eachLink.get(attribute_)
                resourcePath, resourceDomain, conn, filename, outboundLink = self.linkBuilder(link, current_url)
                if resourcePath != None:
                    resourceHTTPS = str(conn) + "://" + str(resourceDomain) + str(resourcePath)
                    if outboundLink is False:
                        if filename != None:
                            try:
                                newResourcePath = f'{page_files}/{filename}'
                                if os.path.exists(newResourcePath) is False:
                                    print(f"/-/ Fetching remote resource {filename} /-/")
                                    obtainedResource = self.request.get(resourceHTTPS, headers=self.HEADERS)
                                    with open(newResourcePath, 'wb') as resourceFile:
                                        resourceFile.write(obtainedResource.content)
                                    root_path = os.getcwd().replace('\\', '/')
                                    eachLink[attribute_] = f'file:///{root_path}/{page_dir}/page_files/{filename}'
                                else:
                                    print(f"/-/ Using cached resource {filename} /-/")
                                    root_path = os.getcwd().replace('\\', '/')
                                    eachLink[attribute_] = f'file:///{root_path}/{page_dir}/page_files/{filename}'
                                eachLink[attribute_] = f''
                            except Exception as e:
                                print(e)
                    else:
                        eachLink[attribute_] = f''
        with open(f'{save_name}/{save_name}.html', 'w', encoding='utf-8') as file:
            file.write(soup.decode())
    
    def generatePDF(self, htmlDir, wkhtmltopdf_exec=r"F:\\GitHub\\bot-lib-public\\wkhtmltox\\bin\\wkhtmltopdf.exe"):
        """
        use wkhtmltopdf to generate a PDF & pdfkit

        Args:
            htmlDir (str): Directory in which html and associated files have been saved
            wkhtmltopdf_exec (str): Absolute path to wkhtmltopdf executable
        """
        pdfkit_config = pdfkit.configuration(wkhtmltopdf=wkhtmltopdf_exec)
        options_ = {
            '--allow':os.getcwd(), 
            '--javascript-delay':3000, 
            '--no-stop-slow-scripts':'', 
            '--enable-local-file-access':'', 
            '--enable-javascript':''
        }
        pdfkit.from_file(f"{htmlDir}/{htmlDir}.html", f"{htmlDir}/{htmlDir}.pdf", options=options_, configuration=pdfkit_config)
    
    def outputPDF(self, htmlDir, pdfName, browser_exec_dir='"C:\\Program Files\\Google\\Chrome\\Application\\"'):
        """
        Use Browser present in the system to generate a PDF

        Args:
            htmlDir (str): Directory where the HTML and files is stored
            pdfName (str): PDF file name
            browser_exec_dir (str): Browser directory where executable is present 
            | - example -> '"C:\\Program Files\\Google\\Chrome\\Application\\"'
        """
        root_path = os.getcwd().replace('\\', '/')
        pdfName = f'"{root_path}/{htmlDir}/{pdfName}"'
        htmlfile = f'"{root_path}/{htmlDir}/{htmlDir}.html"'
        self.setPATH(browser_exec_dir)
        command = 'chrome.exe --headless --disable-gpu --print-to-pdf=' + pdfName + ' ' + htmlfile
        os.system(command)
        print("PDF Generated")

    def setPATH(self, path):
        current_path = os.environ.get("PATH", "")
        new_path_value = path
        path_separator = ";" if os.name == "nt" else ":"
        updated_path = current_path + path_separator + new_path_value
        os.environ["PATH"] = updated_path

    def saveHTML(self, save_name):
        content = self.last_request.content
        soup = BeautifulSoup(content, features="html.parser")
        with open(f'{save_name}.html', 'w', encoding='utf-8') as file:
            file.write(soup.prettify())

    def urlparse(self, url):
        parsed_url = urlparse(url)
        path = parsed_url.path
        filename = None
        outboundLink = False
        try:
            if path.endswith('.html'):
                outboundLink = True
        except Exception:
            outboundLink = False
        try:
            if path[-4] == ".":
                filename = path.split('/')[-1]
        except Exception:
            filename = None
        if path.endswith('.js'):
            filename = path.split('/')[-1]
        domain = parsed_url.netloc
        if parsed_url.scheme == "":
            conn = "https"
        else:
            conn = parsed_url.scheme
        return path, domain, conn, filename, outboundLink

    def linkBuilder(self, url, current_url):
        if isinstance(url, str):
            if url.startswith('//'):
                return self.urlparse(url)
            elif url.startswith('https://'):
                return self.urlparse(url)
            else:
                resourcePath, resourceDomain, conn, filename, outboundLink = self.urlparse(current_url)
                processed_url = deepcopy(resourcePath).split('/')
                final_resource = ""
                pop_last = 1
                for each in url:
                    if final_resource == "../":
                        pop_last = pop_last + 1
                        final_resource = ""
                        final_resource = final_resource + each
                    else:
                        final_resource = final_resource + each
                for each in range(0, pop_last):
                    processed_url.pop(-1)
                urlFound = f"{conn}://{resourceDomain}{'/'.join(processed_url)}/{final_resource}"
                return self.urlparse(urlFound)
        else:
            return None, None, None, None, None
    
    def registerHistory(self, requestContent):
        contentHash = self.hash(requestContent.url)
        history_obj = {
            'url':requestContent.url, 
            'status':requestContent.status_code, 
            'request_tag':contentHash,
            'datetime':str(datetime.now())
        }
        self.HISTORY.append(history_obj)
        self.HISTORY_CONTENT[contentHash] = requestContent
        return True
    
    def clearHistory(self, clearCookies=False):
        if clearCookies:
            self.request.close()
            self.request = requests.Session()
        self.HISTORY = []
        self.HISTORY_CONTENT = {}
    
    def getDomain(self, url):
        return url.replace('http://', '').replace('https://', '').split('/')[0]
    
    def exportHistory(self):
        with open("History/history_saved.hist", 'wb') as f:
            pickle.dump([self.HISTORY, self.HISTORY_CONTENT], f)

    def importHistory(self):
        with open("History/history_saved.hist", 'rb') as f:
            HISTORY_IMPORT = pickle.load(f)
            self.HISTORY = HISTORY_IMPORT[0]
            self.HISTORY_CONTENT = HISTORY_IMPORT[1]
            last_request_tag = self.HISTORY[-1]['request_tag']
            self.last_request = self.HISTORY_CONTENT[last_request_tag]

    def hash(self, string):
        return str(hashlib.md5(string.encode()).hexdigest())

    def saveCookies(self, filename="last_session.cookies"):
        try:
            with open(filename, 'wb') as f:
                pickle.dump(self.request.cookies, f)
            print("Cookies Saved")
        except Exception:
            pass
    
    def loadCookies(self, filename="last_session.cookies"):
        try:
            with open(filename, 'rb') as f:
                self.request.cookies.update(pickle.load(f))
            print("Cookies Loaded")
        except Exception:
            pass

    def mkDir(self, directoryPath):
        try:
            os.mkdir(directoryPath)
            return True, directoryPath
        except Exception:
            return False, directoryPath


if __name__ == "__main__":
    pass