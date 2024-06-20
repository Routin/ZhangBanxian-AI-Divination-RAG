import sys

# 启动大模型
from model.model import LLM
banxian = LLM(use_quantization=True)

# 启动向量数据库
from VectorBase.vector import VectorDatabase
vector_db = VectorDatabase()
vector_db.generate_vector_database("./resource/Gua.txt") # 生成数据库
vector_db.load_vector_database() # 加载数据库

# 起卦并得到卦象和动爻的函数
from utils import divination, prompt

def generate_first_input(question):
    qigua_result = divination.qigua()  # '原卦','卦名','变卦','变卦名','动爻','详细'

    # RAG查询卦象
    query_original = prompt.assemble_query(qigua_result['卦名'])
    query_changed = prompt.assemble_query(qigua_result['变卦名'])

    # 合成首次输入并给模型
    query_result_original = vector_db.query(query_original, k=2)
    query_result_changed = vector_db.query(query_changed, k=2)
    first_input = prompt.assemble_prompt(qigua=qigua_result['详细'],
                                         gua=[qigua_result['卦名'], qigua_result['原卦']],
                                         biangua=[qigua_result['变卦名'], qigua_result['变卦']],
                                         yao=qigua_result['动爻'],
                                         query=[query_result_original, query_result_changed],
                                         question=question)
    return first_input

def read_multiline_input(prompt_text):
    print(prompt_text, end='')
    sys.stdout.flush()
    input_lines = []
    while True:
        line = input()
        if line == '':
            break
        input_lines.append(line)
    return "\n".join(input_lines)

def main():
    while True:
        # 得到用户输入的首个问题
        question = read_multiline_input("请输入您要卜算的疑惑，点击两次回车以发送：\n")
        first_input = generate_first_input(question)
        
        print("张半仙起卦中...")
        print(banxian(first_input))
        
        # 开始多轮对话
        while True:
            user_input = read_multiline_input("请输入您还要向半仙咨询的问题，点击两次回车以发送（输入'退出'或'q'以结束对话，输入'remake'重新起卦）：\n")
            if user_input.lower() in ['退出', 'q', 'quit', 'exit']:
                print("对话结束。")
                return
            elif user_input.lower() == 'remake':
                print("张半仙正在整理算筹...")
                banxian.clean_history()
                break
            
            response = banxian(user_input)
            print(response)

if __name__ == "__main__":
    main()
