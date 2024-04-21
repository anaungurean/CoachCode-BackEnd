import subprocess
import os

def test_code(language, code, input_data):
    file_name = None
    command = None
    if language == "python":
        command = ["python", "-c", code]
    elif language == "java":
        file_name = "Solution.java"
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(code)
        subprocess.run(["javac", file_name], check=True)
        command = ["java", "Solution"]

    try:
        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output, error = process.communicate(input=input_data)
        if process.returncode != 0:
            return {"error": error}
    except subprocess.CalledProcessError as e:
        return {"error": str(e)}

    if file_name:
        os.remove(file_name)
    return output, error


# if __name__ == "__main__":
#     code = '''
# class Solution(object):
#     def twoSum(self, nums, target):
#         """
#         :type nums: List[int]
#         :type target: int
#         :rtype: List[int]
#         """
#         for index_1 in range(0, len(nums)):
#             for index_2 in range(index_1 + 1, len(nums)):
#                 if nums[index_1] + nums[index_2] == target:
#                     return (index_1, index_2)
#
# solution = Solution()
# num_input = input().strip()
# nums = list(map(int, num_input.split()))
# target = int(input().strip())
# print(solution.twoSum(nums, target))
# '''
#     input_data = "2 7 11 15\n9"
#     print(code)
#     print(test_code("python", code, input_data))

#     code = '''
# import java.util.*;
#
# class Solution {
#     public int[] twoSum(int[] nums, int target) {
#         for (int index_1 = 0; index_1 < nums.length; index_1++) {
#             for (int index_2 = index_1 + 1; index_2 < nums.length; index_2++) {
#                 if (nums[index_1] + nums[index_2] == target) {
#                     return new int[]{index_1, index_2};
#                 }
#             }
#         }
#         return new int[0];
#     }
#
#     public static void main(String[] args) {
#         Scanner scanner = new Scanner(System.in);
#
#         System.out.println("Introduceti elementele listei nums separate prin spatiu:");
#         String numInput = scanner.nextLine().trim();
#         String[] numStrings = numInput.split(" ");
#         int[] nums = new int[numStrings.length];
#         for (int i = 0; i < numStrings.length; i++) {
#             nums[i] = Integer.parseInt(numStrings[i]);
#         }
#
#         System.out.println("Introduceti valoarea target: ");
#         int target = scanner.nextInt();
#
#         Solution solution = new Solution();
#         int[] result = solution.twoSum(nums, target);
#         if (result.length == 2) {
#             System.out.println("Indicii perechii care aduna " + target + " sunt: [" + result[0] + ", " + result[1] + "]");
#         } else {
#             System.out.println("Nu s-a gasit nicio pereche cu suma " + target);
#         }
#     }
# }
# '''
#     input_data = "2 7 11 15\n9"
#     print(test_code("java", code, input_data))










