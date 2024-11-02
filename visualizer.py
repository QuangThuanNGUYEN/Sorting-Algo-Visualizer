import tkinter as tk
from tkinter import ttk
import random
import time
import threading

class SortingAlgorithm:
    def __init__(self, data, update_ui_callback):
        self.data = data
        self.update_ui_callback = update_ui_callback
        self._stop_sorting = False

    def sort(self):
        raise NotImplementedError("Sort method not implemented!")

    def stop(self):
        self._stop_sorting = True

    def resume(self):
        self._stop_sorting = False

    def update_ui(self, active_indices=[]):
        if not self._stop_sorting:
            self.update_ui_callback(self.data, active_indices)
            time.sleep(0.1)

class BubbleSort(SortingAlgorithm):
    def sort(self):
        for i in range(len(self.data)):
            for j in range(len(self.data) - i - 1):
                if self._stop_sorting:
                    return
                if self.data[j] > self.data[j + 1]:
                    self.data[j], self.data[j + 1] = self.data[j + 1], self.data[j]
                    self.update_ui([j, j + 1])

class SelectionSort(SortingAlgorithm):
    def sort(self):
        for i in range(len(self.data)):
            min_index = i
            for j in range(i + 1, len(self.data)):
                if self._stop_sorting:
                    return
                if self.data[j] < self.data[min_index]:
                    min_index = j
            if min_index != i:
                self.data[i], self.data[min_index] = self.data[min_index], self.data[i]
                self.update_ui([i, min_index])

class InsertionSort(SortingAlgorithm):
    def sort(self):
        for i in range(1, len(self.data)):
            key = self.data[i]
            j = i - 1
            while j >= 0 and key < self.data[j]:
                if self._stop_sorting:
                    return
                self.data[j + 1] = self.data[j]
                j -= 1
                self.update_ui([j + 1])
            self.data[j + 1] = key
            self.update_ui([j + 1])

class MergeSort(SortingAlgorithm):
    def sort(self):
        self._merge_sort(0, len(self.data) - 1)

    def _merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(left, mid)
            self._merge_sort(mid + 1, right)
            self._merge(left, mid, right)

    def _merge(self, left, mid, right):
        left_copy = self.data[left:mid + 1]
        right_copy = self.data[mid + 1:right + 1]

        left_index, right_index = 0, 0
        sorted_index = left

        while left_index < len(left_copy) and right_index < len(right_copy):
            if self._stop_sorting:
                return
            if left_copy[left_index] <= right_copy[right_index]:
                self.data[sorted_index] = left_copy[left_index]
                left_index += 1
            else:
                self.data[sorted_index] = right_copy[right_index]
                right_index += 1
            self.update_ui([sorted_index])
            sorted_index += 1

        while left_index < len(left_copy):
            if self._stop_sorting:
                return
            self.data[sorted_index] = left_copy[left_index]
            left_index += 1
            self.update_ui([sorted_index])
            sorted_index += 1

        while right_index < len(right_copy):
            if self._stop_sorting:
                return
            self.data[sorted_index] = right_copy[right_index]
            right_index += 1
            self.update_ui([sorted_index])
            sorted_index += 1

class QuickSort(SortingAlgorithm):
    def sort(self):
        self._quick_sort(0, len(self.data) - 1)

    def _quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self._quick_sort(low, pi - 1)
            self._quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.data[high]
        i = low - 1
        for j in range(low, high):
            if self._stop_sorting:
                return
            if self.data[j] < pivot:
                i += 1
                self.data[i], self.data[j] = self.data[j], self.data[i]
                self.update_ui([i, j])
        self.data[i + 1], self.data[high] = self.data[high], self.data[i + 1]
        self.update_ui([i + 1, high])
        return i + 1

class HeapSort(SortingAlgorithm):
    def sort(self):
        n = len(self.data)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)
        for i in range(n - 1, 0, -1):
            self.data[i], self.data[0] = self.data[0], self.data[i]
            self.update_ui([i, 0])
            self.heapify(i, 0)

    def heapify(self, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self.data[left] > self.data[largest]:
            largest = left
        if right < n and self.data[right] > self.data[largest]:
            largest = right
        if largest != i:
            self.data[i], self.data[largest] = self.data[largest], self.data[i]
            self.update_ui([i, largest])
            self.heapify(n, largest)

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithms Visualizer")
        self.root.geometry("800x700")
        self.array = []
        self.speed = tk.DoubleVar(value=0.1)
        self.sorting_algorithm = None
        self.sorting_thread = None
        self.paused = False
        self.create_widgets()
        self.update_array()

    def create_widgets(self):
        control_frame = ttk.Frame(self.root)
        control_frame.pack(pady=10)

        ttk.Label(control_frame, text="Algorithm:").grid(row=0, column=0)
        self.algo_choice = ttk.Combobox(control_frame, values=["Bubble Sort", "Selection Sort", "Insertion Sort", "Merge Sort", "Quick Sort", "Heap Sort"], state="readonly")
        self.algo_choice.grid(row=0, column=1)
        self.algo_choice.current(0)

        ttk.Label(control_frame, text="Speed:").grid(row=1, column=0)
        speed_scale = ttk.Scale(control_frame, from_=0.01, to=0.5, variable=self.speed)
        speed_scale.grid(row=1, column=1)

        ttk.Button(control_frame, text="Generate Random Data", command=self.update_array).grid(row=2, column=0, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Enter Data", command=self.enter_data_manually).grid(row=3, column=0, columnspan=2, pady=5)

        ttk.Button(control_frame, text="Start", command=self.start_sorting_thread).grid(row=4, column=0, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Stop", command=self.stop_sorting).grid(row=5, column=0, columnspan=2, pady=5)
        ttk.Button(control_frame, text="Resume", command=self.resume_sorting).grid(row=6, column=0, columnspan=2, pady=5)

        self.canvas = tk.Canvas(self.root, width=780, height=400, bg="white")
        self.canvas.pack(pady=10)

    def update_array(self, size=20):
        self.array = [random.randint(1, 100) for _ in range(size)]
        self.draw_array()

    def enter_data_manually(self):
        manual_data_window = tk.Toplevel(self.root)
        manual_data_window.title("Enter Data")
        
        tk.Label(manual_data_window, text="Enter numbers separated by commas:").pack(pady=5)
        entry = tk.Entry(manual_data_window, width=50)
        entry.pack(pady=5)
        
        def set_manual_data():
            data_str = entry.get()
            try:
                self.array = list(map(int, data_str.split(',')))
                self.draw_array()
                manual_data_window.destroy()
            except ValueError:
                tk.messagebox.showerror("Invalid Input", "Please enter only integers separated by commas.")
        
        tk.Button(manual_data_window, text="Set Data", command=set_manual_data).pack(pady=5)

    def draw_array(self, active_indices=[], color="blue", active_color="red"):
        self.canvas.delete("all")
        c_height = 400
        c_width = 780
        bar_width = c_width / (len(self.array) + 1)
        
        for i, val in enumerate(self.array):
            x0 = i * bar_width + 10
            y0 = c_height - val * 3
            x1 = (i + 1) * bar_width + 10
            y1 = c_height
            color_to_use = active_color if i in active_indices else color
            self.canvas.create_rectangle(x0, y0, x1, y1, fill=color_to_use)

    def start_sorting_thread(self):
        if self.sorting_thread is not None and self.sorting_thread.is_alive():
            return  # Already sorting
        algorithm_name = self.algo_choice.get()
        if algorithm_name == "Bubble Sort":
            self.sorting_algorithm = BubbleSort(self.array.copy(), self.update_ui)
        elif algorithm_name == "Selection Sort":
            self.sorting_algorithm = SelectionSort(self.array.copy(), self.update_ui)
        elif algorithm_name == "Insertion Sort":
            self.sorting_algorithm = InsertionSort(self.array.copy(), self.update_ui)
        elif algorithm_name == "Merge Sort":
            self.sorting_algorithm = MergeSort(self.array.copy(), self.update_ui)
        elif algorithm_name == "Quick Sort":
            self.sorting_algorithm = QuickSort(self.array.copy(), self.update_ui)
        elif algorithm_name == "Heap Sort":
            self.sorting_algorithm = HeapSort(self.array.copy(), self.update_ui)

        self.sorting_thread = threading.Thread(target=self.sorting_algorithm.sort)
        self.sorting_thread.start()

    def stop_sorting(self):
        if self.sorting_algorithm:
            self.sorting_algorithm.stop()

    def resume_sorting(self):
        if self.sorting_algorithm:
            self.sorting_algorithm.resume()

    def update_ui(self, data, active_indices):
        self.array = data
        self.draw_array(active_indices)

if __name__ == "__main__":
    root = tk.Tk()
    visualizer = SortingVisualizer(root)
    root.mainloop()
