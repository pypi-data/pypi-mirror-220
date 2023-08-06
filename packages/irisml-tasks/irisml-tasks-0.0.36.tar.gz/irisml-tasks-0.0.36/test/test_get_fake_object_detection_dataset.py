import unittest
from irisml.tasks.get_fake_object_detection_dataset import Task


class TestGetFakeObjectDetectionDataset(unittest.TestCase):
    def test_simple(self):
        outputs = Task(Task.Config(num_images=100, num_classes=10, num_max_boxes=10)).execute(None)
        dataset = outputs.dataset
        self.assertEqual(len(dataset), 100)
        self.assertEqual(len(outputs.class_names), 10)
        class_set = set(int(t[0]) for x in dataset for t in x[1])
        self.assertEqual(len(class_set), 10)
        self.assertTrue(all(len(x[1]) <= 10 for x in dataset))
        self.assertLess(sum(len(x[1]) for x in dataset), 1000)
        self.assertTrue(all(len(x[1].shape) == 2 for x in dataset))
        self.assertTrue(all(0 <= x[1] < x[3] <= 1 for _, t in dataset for x in t))
        self.assertTrue(all(0 <= x[2] < x[4] <= 1 for _, t in dataset for x in t))

    def test_multiple_image_sizes(self):
        outputs = Task(Task.Config(image_sizes=[(8, 8), (24, 24), (16, 16), (64, 2)])).execute(None)
        image_sizes_set = set(image.size for image, _ in outputs.dataset)
        self.assertEqual(image_sizes_set, {(8, 8), (24, 24), (16, 16), (64, 2)})

    def test_random_seed(self):
        outputs1 = Task(Task.Config(num_images=100, random_seed=0)).execute(Task.Inputs())
        outputs2 = Task(Task.Config(num_images=100, random_seed=0)).execute(Task.Inputs())

        targets1 = [d[1].tolist() for d in outputs1.dataset]
        targets2 = [d[1].tolist() for d in outputs2.dataset]
        self.assertEqual(targets1, targets2)

        outputs3 = Task(Task.Config(num_images=100, random_seed=1)).execute(Task.Inputs())
        targets3 = [d[1].tolist() for d in outputs3.dataset]
        self.assertNotEqual(targets1, targets3)
