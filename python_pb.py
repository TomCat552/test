"""
file_src：pb二进制文件
file_des：txt明文文件
"""
def pb_2_txt(self, binary_conf, file_src, file_des):
    """
    从pb中读取数据文件
    binary_conf 配置信息
    file_src 二进制文件
    file_des 明文文件存储位置
    """
    # 指明引入的包：proto生成的py文件
    import pb2
    if len(binary_conf['message']) > 0:
        try:
            # pb_message：就是生成的py文件中的对象
            pb_message = eval(binary_conf['message'])
        except NameError:
            print_utils.print_warning('[FATAL] pb name not found: %s, quit' % binary_conf['message'])
            exit(1)
        except AttributeError:
            print_utils.print_warning('[FATAL] pb attribute not found: %s, quit' % binary_conf['message'])
            exit(1)
    else:
        print_utils.print_warning('[FATAL] message not found: %s, quit')
        exit(1)
    
    if len(binary_conf['message_name']) > 0:
        try:
            message_name = binary_conf['message_name']
        except NameError:
            print_utils.print_warning('[FATAL] pb message_name not found: %s, quit' % binary_conf['message_name'])
            exit(1)
        except AttributeError:
            print_utils.print_warning('[FATAL] pb attribute not found: %s, quit' % binary_conf['message_name'])
            exit(1)
    else:
        print_utils.print_warning('[FATAL] message_name not found: %s, quit')
        exit(1)
 
    mesasge_list = []
    
    """
    方法一：读取pb数据，写入文件，不转为dict，解决bytes类型数据转换失败的问题
    1、二进制数据反序列化
    2、反序列化数据写入临时文件 temp
    3、读取临时文件，转换为标准行列式，写入明文文件
    4、删除临时文件
    """ 
    try:
        # 1、二进制反序列化
        with open(file_src, 'rb') as bf:
            binary_data = bf.read()
            # 反序列化
            pb_message.ParseFromString(binary_data)
    except Exception as e:
        traceback.print_exc()
        print_utils.print_warning('[FATAL] ParseFromString fail: %s, quit' % binary_conf['message'])
        exit(1)
    try:
        # 2、反序列化数据写入临时文件
        with open(file_des + '.temp', 'w') as tf:
            tf.write(str(pb_message))
    except Exception as e:
        traceback.print_exc()
        print_utils.print_warning('[FATAL] write temp file fail: %s, quit' % binary_conf['message'])
        exit(1)
    try:
        # 读取临时文件，写入明文文件，转换为标准行列式
        with open(file_des + '.temp', 'r') as tf:
            mesasge_list = []
            temp_list = []
            temp_content = tf.readlines()
            for line in temp_content:
                line = line.strip('\n')
                # 根据message_name区分,过滤首尾行,例如：coach_lines { }
                if '{' in line: # 首行
                    continue
                if '}' in line: # 尾行
                    # 写入message_list
                    mesasge_list.append(binary_conf['split'].join(temp_list))
                    temp_list = []
                else:
                    # 非首尾行，写入
                    temp_list.append(line.split(': ')[1])
            # 写入明文文件
            self.write_all(file_des, mesasge_list)
    except Exception as e:
        traceback.print_exc()
        print_utils.print_warning('[FATAL] write txt file fail: %s, quit' % binary_conf['message'])
        exit(1)
    try:
        # 删除temp临时文件
        os.remove(file_des + '.temp')
    except Exception as e:
        print_utils.print_warning('[WARNING] remove temp file fail: %s, quit' % binary_conf['message'])
        exit(1)
                
    # 方法二：pb转dict，有问题：bytes类型的数据protobuf_to_dict转换有问题
    # try:
    #     with open(file_src, 'rb') as bf:
    #         # 二进制文件数据
    #         binary_data = bf.read()
    #         # 反序列化
    #         pb_message.ParseFromString(binary_data)
    #         # pb转dict
    #         dict_data = protobuf_to_dict(pb_message)
    #         # 处理dict，写入明文文件中
    #         coach_graphs = dict_data[message_name]
    #         for graphDic in coach_graphs:
    #             # print(graphDic)
    #             # exit(1)
    #             message = []
    #             # 处理common字段
    #             if len(binary_conf['common']) > 0:
    #                 count = 0
    #                 for common_field in binary_conf['common']:
    #                     if count > 10:
    #                         exit(1)
    #                     msg_type = common_field.split(' ')[0]
    #                     msg_content = graphDic[common_field.split(' ')[1]]
    #                     # # bytes字段转为字符串
    #                     if msg_type == 'bytes':
    #                         print('------')
    #                         print(("b'" + msg_content).decode())
    #                         exit(1)
    #                         message.append(str(msg_content.decode("utf-8")))
    #                         # message.append(str(msg_content.decode("utf-8").decode('gbk').encode('utf-8')))
    #                     else:
    #                         message.append(str(msg_content))
    #                     # print(msg_type)
    #                     # print(msg_content)
    #                     count += 1
    #             # 处理repeated字段
    #             if len(binary_conf['repeated']) > 0:
    #                 for common_field in binary_conf['repeated']:
    #                     for line_sid in graphDic[common_field.split(' ')[1]]:
    #                         # message.append(str(line_sid.decode("gbk")))  # aaa.decode("gbk")
    #                         message.append(str(line_sid))
    #             mesasge_list.append(binary_conf['split'].join(message))
    #         self.write_all(file_des, mesasge_list)
    # except Exception as e:
    #     traceback.print_exc()
    #     print_utils.print_warning('[FATAL] ParseFromString fail: %s, quit' % binary_conf['message'])
    #     exit(1)
