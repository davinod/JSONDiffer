#!../venv/bin/python

import unittest
import requests

from differ import Differ
from diffresult import DiffResult, Offset

global validJSON
global validJSON2
global invalidJSON

#Saving a valid an invalid JSON content in base64
validJSON='ew0KCSJnbG9zc2FyeSI6IHsNCgkJInRpdGxlIjogInRlc3QgMyIsDQoJCSJuYW1lIjogImRhdmkiLA0KCQkiYWdlIjogIjMzIg0KCX0NCn0='
validJSON2='ew0KCSJnbG9zc2FyeSI6IHsNCgkJInRpdGxlIjogInRlc3QgMSIsDQoJCSJuYW1lIjogImRhdmkiLA0KCQkiYWdlIjogIjMyIg0KCX0NCn0='
validJSONDiffSize='ew0KCSJnbG9zc2FyeSI6IHsNCgkJInRpdGxlIjogInRlc3QgMSIsDQoJCSJuYW1lIjogImRhdmkgZGlvZ28iLA0KCQkiYWdlIjogIjMyIg0KCX0NCn0='
invalidJSON='eyBnbG9zc2FyeSI6IHsJInRpdGxlIjogImV4YW1wbGUgZ2xvc3NhcnkiCX0gfQ=='


class TestJSONDifferClass(unittest.TestCase):

    def test_ValidJSONs(self):
        differ = Differ()

        #Empty jsons must fail the validation
        self.assertEqual(differ.isLeftValid(),"false", "Expected left invalid when empty")
        self.assertEqual(differ.isRightValid(), "false", "Expected right invalid when empty")

        #Invalid jsons must fail the validation
        differ.left = invalidJSON
        differ.right = invalidJSON
        self.assertEqual(differ.isLeftValid(), "false", "Expected left invalid")
        self.assertEqual(differ.isRightValid(), "false", "Expected right invalid")

        #Valid jsons must pass the validation
        differ.left = validJSON
        differ.right = validJSON
        self.assertEqual(differ.isLeftValid(), "true", "Expected left valid")
        self.assertEqual(differ.isRightValid(), "true", "Expected right valid")

    def test_Diffs(self):
        differ = Differ()

        #Test equal content
        differ.left = validJSON
        differ.right = validJSON
        self.assertIn("left and right are equal", differ.Diff(), "Expected equal content")

        #Test diff size
        differ.left = validJSON
        differ.right = validJSONDiffSize
        self.assertIn("sizes are different", differ.Diff(), "Expected different size")

        #Test same size diff contents
        differ.left = validJSON
        differ.right = validJSON2
        self.assertIn("Sizes are equal but contents different", differ.Diff(), "Expected different contents")
        self.assertIn("offset", differ.Diff(), "Expected different contents")


class TestHTTPURIs(unittest.TestCase):

    def test_index(self):
        resp = requests.get('http://localhost:5000/v1/index')
        self.assertEqual(resp.status_code, 200, "Expected response code 200 for index")

    def test_setleft(self):
        resp = requests.get('http://localhost:5000/v1/diff/setleft')
        self.assertEqual(resp.status_code, 200, "Expected response code 200 for setleft")

    def test_setright(self):
        resp = requests.get('http://localhost:5000/v1/diff/setright')
        self.assertEqual(resp.status_code, 200, "Expected response code 200 for setright")

    def test_right(self):
        #I was expecting that the redirect would result in code 302
        # but apparently it comes 200 - perhaps because of the result of the page requested by the redirect
        resp = requests.get('http://localhost:5000/v1/diff/right/aaaaa')
        self.assertEqual(resp.status_code, 200, "Expected response code 200 for right")

    def test_left(self):
        #I was expecting that the redirect would result in code 302
        # but apparently it comes 200 - perhaps because of the result of the page requested by the redirect
        resp = requests.get('http://localhost:5000/v1/diff/left/aaaa')
        self.assertEqual(resp.status_code, 200, "Expected response code 200 for left")

    def test_diff(self):
        #I was expecting that the redirect would result in code 302
        # but apparently it comes 200 - perhaps because of the result of the page requested by the redirect
        resp = requests.get('http://localhost:5000/v1/diff')
        self.assertEqual(resp.status_code, 200, "Expected response code 200 for left")

class TestDiffGetState(unittest.TestCase):

    # 22 - left empty, right empty
    # 21 - left empty, right invalid
    # 20 - left empty, right valid
    # 12 - left invalid, right empty
    # 11 - left invalid, right invalid
    # 10 - left invalid, right valid
    # 02 - left valid, right empty
    # 01 - left valid, right invalid
    # 00 - left valid, right valid :)

    def test_getState(self):

        differ = Differ()

        differ.left=""
        differ.right=""
        self.assertEqual(differ.getState(), "22", "Expected getState 22")

        differ.left=""
        differ.right=invalidJSON
        self.assertEqual(differ.getState(), "21", "Expected getState 21")

        differ.left=""
        differ.right=validJSON
        self.assertEqual(differ.getState(), "20", "Expected getState 20")

        differ.left=invalidJSON
        differ.right=""
        self.assertEqual(differ.getState(), "12", "Expected getState 12")

        differ.left=invalidJSON
        differ.right=invalidJSON
        self.assertEqual(differ.getState(),"11", "Expected getState 11")

        differ.left=invalidJSON
        differ.right=validJSON
        self.assertEqual(differ.getState(),"10", "Expected getState 10")

        differ.left=validJSON
        differ.right=""
        self.assertEqual(differ.getState(),"02", "Expected getState 02")

        differ.left=validJSON
        differ.right=invalidJSON
        self.assertEqual(differ.getState(), "01", "Expected getState 01")

        differ.left=validJSON
        differ.right=validJSON
        self.assertEqual(differ.getState(), "00", "Expected getState 00")

class TestDiffResult(unittest.TestCase):
    def test_EqualResultMsg(self):
        diffresult = DiffResult()
        diffresult.decodedleft = validJSON
        diffresult.decodedright= validJSON
        self.assertEqual(diffresult.__str__(), diffresult.GetEqualResultMsg(),"Expected equal result message for same json contents")

    def test_DiffSizeMsg(self):
        diffresult = DiffResult()
        diffresult.decodedleft = validJSON
        diffresult.decodedright= validJSON + "aaa" #adding 3 bytes
        self.assertEqual(diffresult.__str__(), diffresult.GetDifferentSizeMsg(),"Expected different size message for different json sizes")

    def test_DiffSameSizeDiffContents(self):
        diffresult = DiffResult()
        diffresult.decodedleft = validJSON
        diffresult.decodedright= validJSON[:-1] + "*" #Change the last char and keep the same size

        #create few offsets
        offsets = list()
        offset = Offset()

        offsets.append(Offset(10,100,2))
        offsets.append(Offset(20,400,3))
        offsets.append(Offset(25,460,1))

        diffresult.offsets = offsets

        self.assertEqual(diffresult.__str__(), diffresult.GetEqualSizeDiffResultMsg(),"Expected diff result message for diff json contents with same size")



if __name__ == '__main__':
    unittest.main()

