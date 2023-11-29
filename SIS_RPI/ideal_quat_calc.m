ideal_quat = []
for i = 1 : 100
    sis_file = load(sprintf("./Output/SIS_iter_%s.mat", string(i)))
    sis_input_attitude = sis_file.sis_input_attitude
    q = angle2quat(deg2rad(sis_input_attitude(1)), deg2rad(-sis_input_attitude(2)), deg2rad(-sis_input_attitude(3)), 'ZYX');
    q_ref = [q(2:4) q(1)];
    ideal_quat = [ideal_quat; q_ref]
end
writematrix(ideal_quat, "ideal_quat.txt")