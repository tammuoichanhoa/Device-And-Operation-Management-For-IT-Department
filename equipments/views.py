# from django.shortcuts import render
# from django.db.models import Count, Q, Avg, Max, Min, Sum
# from django.db.models.functions import TruncYear, Coalesce
# from .models import Equipment, ConsumableEquipment, NetworkDevice
# from django.contrib.admin.views.decorators import staff_member_required
# from common.models import Department
# import json
# from django.conf import settings
# from django.utils import timezone


# @staff_member_required
# def equipment_stats_view(request):
#     total_equipment = Equipment.objects.count()
#     total_available = Equipment.objects.filter(available=True).count()
#     total_not_available = Equipment.objects.filter(available=False).count()
#     total_with_warranty = Equipment.objects.exclude(expiry_date=None).count()
    
#     quality_dict = dict(settings.QUALIFICATIONS)
#     network_dict = dict(settings.COMPUTER_NETWORKS)
#     # Lấy danh sách các phòng ban cấp thấp nhất (leaf nodes)
#     leaf_departments = Department.objects.filter(children__isnull=True)
    

#     # Thống kê thiết bị theo các phòng ban cấp thấp nhất
#     by_department = (
#         Equipment.objects
#         .filter(department__in=leaf_departments)
#         .values('department__id')
#         .annotate(total=Count('serial'))
#         .order_by('-total')
#     )
#     print(by_department)
#     # Xử lý các giá trị None
#     for item in by_department:
#         if item['department__id'] is None:
#             item['department__id'] = "Chưa xác định"
    
#     # Thống kê theo nhóm thiết bị
#     by_group = list(Equipment.objects.values('group')
#                    .annotate(total=Count('serial'))
#                    .order_by('-total'))
    
#     # Xử lý các giá trị None trong group
#     for item in by_group:
#         if item['group'] is None:
#             item['group'] = "Chưa xác định"
    
#     # Thống kê theo năm đưa vào sử dụng
#     by_year = list(Equipment.objects.exclude(year=None)
#                   .values('year')
#                   .annotate(total=Count('serial'))
#                   .order_by('year'))
    
#     # Thêm vào danh sách "Không rõ năm"
#     unknown_year_count = Equipment.objects.filter(year=None).count()
#     if unknown_year_count > 0:
#         by_year.append({'year': None, 'total': unknown_year_count})
    
#     # Thống kê theo loại trang bị (ktdb)
#     by_type = list(Equipment.objects.values('ktdb')
#                   .annotate(total=Count('serial'))
#                   .order_by('-total'))
    
#     # Xử lý các giá trị None trong ktdb
#     for item in by_type:
#         if item['ktdb'] is None:
#             item['ktdb'] = "Chưa phân loại"
    
#     # # Thống kê theo xuất xứ
#     # by_country = list(Equipment.objects.values('country')
#     #                  .annotate(total=Count('serial'))
#     #                  .order_by('-total'))
    
#     # # Xử lý các giá trị None trong country
#     # for item in by_country:
#     #     if item['country'] is None:
#     #         item['country'] = "Chưa xác định"
    
#     # Thống kê theo tình trạng bảo hành
#     warranty_status = [
#         {
#             'status': 'Còn bảo hành',
#             'total': Equipment.objects.filter(expiry_date__gt=timezone.now()).count()
#         },
#         {
#             'status': 'Hết bảo hành',
#             'total': Equipment.objects.filter(expiry_date__lte=timezone.now()).count()
#         },
#         {
#             'status': 'Không có thông tin',
#             'total': Equipment.objects.filter(expiry_date=None).count()
#         }
#     ]
    
#     # Thống kê theo chất lượng (PCCL)
#     by_quality = list(Equipment.objects.values('quality')
#                      .annotate(total=Count('serial'))
#                      .order_by('-total'))
    
#     # === BỔ SUNG THỐNG KÊ VẬT TƯ TIÊU HAO ===
#     # Tổng số vật tư tiêu hao
#     total_consumables = ConsumableEquipment.objects.count()

    
#     # Thống kê vật tư tiêu hao theo phòng ban
#     consumables_by_department = (
#         ConsumableEquipment.objects
#         .filter(equipment__department__in=leaf_departments)
#         .select_related('equipment__department')
#         .values('equipment__department__id')
#         .annotate(
#             total_items=Count('id'),
#             total_quantity=Sum('quantity')
#         )
#         .order_by('-total_quantity')
#     )
    
#     # Xử lý các giá trị None
#     for item in consumables_by_department:
#         if item['equipment__department__id'] is None:
#             item['equipment__department__id'] = "Chưa xác định"
    
#     # === BỔ SUNG THỐNG KÊ THIẾT BỊ MẠNG ===
#     # Tổng số thiết bị mạng
#     total_network_devices = NetworkDevice.objects.count()
    
#     # Thống kê thiết bị mạng theo tên mạng (từ constant)
#     network_devices_by_network = (
#         NetworkDevice.objects
#         .values('network')  # 'network' là CharField chứ không còn là ForeignKey
#         .annotate(total=Count('id'))
#         .order_by('-total')
#     )
    
#     # Xử lý các giá trị None
#     for item in network_devices_by_network:
#         network_code = item['network']
#         if network_code is None:
#             item['network'] = "Mạng chưa xác định"
#         else:
#             item['network'] = network_dict.get(network_code, network_code)  # fallback nếu không có trong constant
    

    
    

#     # Chuẩn bị context để truyền vào template
#     context = {
#         # Tổng quan
#         "total_equipment": total_equipment,
#         "total_available": total_available,
#         "total_not_available": total_not_available,
#         "total_with_warranty": total_with_warranty,
        
#         # Thống kê theo đơn vị
#         "departments": json.dumps([i['department__id'] for i in by_department]),
#         "departments_data": json.dumps([i['total'] for i in by_department]),
        
#         # Thống kê theo nhóm
#         "groups": json.dumps([i['group'] for i in by_group]),
#         "groups_data": json.dumps([i['total'] for i in by_group]),
        
#         # Thống kê theo năm
#         "years": json.dumps([str(i['year']) if i['year'] is not None else "Không rõ" for i in by_year]),
#         "years_data": json.dumps([i['total'] for i in by_year]),
        
#         # Thống kê theo loại
#         "types": json.dumps([i['ktdb'] for i in by_type]),
#         "types_data": json.dumps([i['total'] for i in by_type]),
        
#         # Thống kê theo tình trạng bảo hành
#         "warranty_status": json.dumps([i['status'] for i in warranty_status]),
#         "warranty_data": json.dumps([i['total'] for i in warranty_status]),

#         # Top vật tư tiêu hao
#         "top_consumables": json.dumps([i['name'] for i in top_consumables_data]),
#         "top_consumables_data": json.dumps([i['quantity'] for i in top_consumables_data]),

#         # === THÔNG TIN BỔ SUNG VẬT TƯ TIÊU HAO ===
#         "total_consumables": total_consumables,
#         "total_consumable_quantity": total_consumable_quantity,
#         # "zero_quantity_consumables": zero_quantity_consumables,
        
#         # Thống kê vật tư tiêu hao theo phòng ban
#         "consumables_departments": json.dumps([i['equipment__department__id'] for i in consumables_by_department]),
#         "consumables_departments_items": json.dumps([i['total_items'] for i in consumables_by_department]),
#         "consumables_departments_quantity": json.dumps([i['total_quantity'] for i in consumables_by_department]),
        
#         # === THÔNG TIN BỔ SUNG THIẾT BỊ MẠNG ===
#         "total_network_devices": total_network_devices,
        
#         # Thống kê thiết bị mạng theo mạng máy tính
#         "networks": json.dumps([i['network'] for i in network_devices_by_network]),
#         "networks_data": json.dumps([i['total'] for i in network_devices_by_network]),
        
        
#         # Thống kê thiết bị mạng theo loại thiết bị
#         "network_device_types": json.dumps([i['equipment__ktdb'] for i in network_devices_by_type]),
#         "network_device_types_data": json.dumps([i['total'] for i in network_devices_by_type]),
#     }
    
#     return render(request, "admin/equipment_stats.html", context)