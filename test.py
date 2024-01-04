import pyzed.sl as sl

if __name__ == "__main__":
    # connection_18 = '['
    # for BODY_BONE in sl.BODY_18_BONES:
    #     # MATLAB INDEX
    #     connection_18 += str(BODY_BONE[0].value+1) + ' ' + str(BODY_BONE[1].value+1) + ';'
    # connection_18 = connection_18[:-1]
    # connection_18 += ']'
    # print(connection_18)
    # joints_18 = '['
    # for BODY_PART in list(sl.BODY_18_PARTS):
    #     joints_18 += '\"'+BODY_PART.name+ '\",'
    # joints_18 = joints_18[:-1]
    # joints_18 += ']'
    # print(joints_18)

    # connection_34 = '['
    # for BODY_BONE in sl.BODY_34_BONES:
    #     # MATLAB INDEX
    #     connection_34 += str(BODY_BONE[0].value+1) + \
    #         ' ' + str(BODY_BONE[1].value+1) + ';'
    # connection_34 = connection_34[:-1]
    # connection_34 += ']'
    # print(connection_34)
    # joints_34 = '['
    # for BODY_PART in list(sl.BODY_34_PARTS):
    #     joints_34 += '\"'+BODY_PART.name + '\",'
    # joints_34 = joints_34[:-1]70
    # joints_34 += ']'
    # print(joints_34)

    # connection_70 = '['
    # for BODY_BONE in sl.BODY_70_BONES:
    #     # MATLAB INDEX
    #     connection_70 += str(BODY_BONE[0].value+1) + \
    #         ' ' + str(BODY_BONE[1].value+1) + ';'
    # connection_70 = connection_70[:-1]
    # connection_70 += ']'
    # print(connection_70)
    # joints_70 = '['
    # for BODY_PART in list(sl.BODY_70_PARTS):
    #     joints_70 += '\"'+BODY_PART.name + '\",'
    # joints_70 = joints_70[:-1]
    # joints_70 += ']'
    # print(joints_70)

    connection_38 = '['
    for BODY_BONE in sl.BODY_38_BONES:
        # MATLAB INDEX
        connection_38 += str(BODY_BONE[0].value+1) + \
            ' ' + str(BODY_BONE[1].value+1) + ';'
    connection_38 = connection_38[:-1]
    connection_38 += ']'
    print(connection_38)
    joints_38 = '['
    for BODY_PART in list(sl.BODY_38_PARTS):
        joints_38 += '\"'+BODY_PART.name + '\",'
    joints_38 = joints_38[:-1]
    joints_38 += ']'
    print(joints_38)
