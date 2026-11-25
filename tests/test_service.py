import unittest
from isotope_clusters import process


class IsotopeTests(unittest.TestCase):
    def base(self):
        return {"max_charge":3,"tolerance_mz":"0.01","peaks":[{"id":"p1","mz":"100","intensity":"10"},{"id":"p2","mz":"100.5","intensity":"8"},{"id":"p3","mz":"101","intensity":"5"},{"id":"noise","mz":"103","intensity":"1"}]}
    def test_assigns_charge_two_cluster(self):
        row=process(self.base())["clusters"][0]
        self.assertEqual((row["charge"],row["peak_ids"],row["total_intensity"]),(2,["p1","p2","p3"],"23"))
    def test_noise_remains_unassigned(self):
        self.assertEqual(process(self.base())["unassigned_peak_ids"],["noise"])
    def test_tolerance_accepts_small_error(self):
        data=self.base(); data["peaks"][1]["mz"]="100.505"
        self.assertEqual(process(data)["clusters"][0]["max_spacing_error_mz"],"1/200")
    def test_too_large_error_changes_charge_hypothesis(self):
        data=self.base(); data["peaks"][1]["mz"]="100.52"
        result=process(data)
        self.assertEqual((result["clusters"][0]["charge"],result["clusters"][0]["peak_ids"]),(1,["p1","p3"]))
        self.assertEqual(result["unassigned_peak_ids"],["p2","noise"])
    def test_mz_must_increase(self):
        data=self.base(); data["peaks"][1]["mz"]="99"
        with self.assertRaises(ValueError): process(data)
    def test_duplicate_ids_fail(self):
        data=self.base(); data["peaks"][1]["id"]="p1"
        with self.assertRaises(ValueError): process(data)

if __name__=="__main__": unittest.main()
