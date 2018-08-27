# -*- coding: utf-8 -*-
# author = 'BlackSesion'

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class ChileautosItem(Item):
    id = Field()
    tipo_anuncio = Field()
    url = Field()
    header_nombre = Field()
    ano = Field()
    marca = Field()
    modelo = Field()
    version = Field()
    version_sii = Field()
    precio = Field()
    precio_hoy = Field()
    kilometros = Field()
    categoria = Field()
    carroceria = Field()
    transmision = Field()
    region = Field()
    comentarios = Field()
    vendido = Field()
    fecha_publicacion = Field()
    fecha_creacion = Field()
    fecha_edicion = Field()
    fecha_precio = Field()
    img_url = Field()

    # detalles destacados
    vehiculo_det = Field()
    precio_det = Field()
    kilometros_det = Field()
    color_exterior_det = Field()
    transmision_det = Field()
    puertas_det = Field()
    puertas = Field()
    pasajeros_det = Field()
    pasajeros = Field()
    combustible_det = Field()
    consumo_det = Field()
    region_det = Field()
    ciudad_det = Field()

    # especificaciones - cargos
    cargos_e_c = Field()
    cargos_nombre_impuesto_e_c = Field()
    cargos_monto_impuesto_e_c = Field()
    transporte_e_c = Field()
    transporte_tipo_e_c = Field()
    transporte_monto_e_c = Field()

    # especificaciones - codigo jato
    jato_code_e_cj = Field()
    ano_modelo_e_cj = Field()
    pais_e_cj = Field()
    marca_e_cj = Field()
    modelos_e_cj = Field()
    tipo_vehiculo_e_cj = Field()
    generacion_modelo_e_cj = Field()
    nvl_equip_e_cj = Field()
    numero_puertas_e_cj = Field()
    tipo_carroceria_e_cj = Field()
    plazas_e_cj = Field()
    ruedas_motrices_e_cj = Field()
    litros_e_cj = Field()
    num_cilindros_e_cj = Field()
    crompresor_e_cj = Field()
    tipo_combustible_e_cj = Field()
    potencia_max_e_cj = Field()
    tipo_transmision_e_cj = Field()
    velocidades_e_cj = Field()
    rating_peso_bruto_vehicular_e_cj = Field()
    grupo_modelo_e_cj = Field()

    # especificaciones - combustible
    alimentacion_comb = Field()
    alimentacion_inyeccion_comb = Field()
    combustible_comb = Field()
    combustible_tipo_comb = Field()
    combustible_tipo_prim_comb = Field()
    deposito_c_comb = Field()
    deposito_c_tipo_comb = Field()
    deposito_c_cap_comb = Field()
    deposito_c_lpg_comb = Field()
    deposito_c_cap1_comb = Field()
    deposito_c_cap2_comb = Field()

    # especificaciones - desempeño
    prestaciones_des = Field()
    potencia_des = Field()
    potencia_max1_des = Field()
    potencia_max2_des = Field()
    potencia_reg_des = Field()
    potencia_par_max_des = Field()
    potencia_reg_par_max_des = Field()
    potencia_comb_des = Field()
    consumo_comb_des = Field()
    consumo_comb_standar_des = Field()

    # especificaciones - detalles
    tipo_vehiculo_det = Field()
    tipo_categoria_det = Field()
    version_det = Field()

    # especificaciones - dimensiones
    dim_ext = Field()
    dim_ext_largo = Field()
    dim_ext_ancho = Field()
    dim_ext_alto = Field()
    dim_ext_dist_ejes = Field()
    dim_ext_trocha_del = Field()
    dim_ext_trocha_tra = Field()
    dim_ext_diam_giro = Field()
    dim_cap_baul = Field()
    dim_cap_baul_techo = Field()
    dim_ext_largo2 = Field()
    dim_ext_ancho2 = Field()
    dim_ext_alto2 = Field()
    dim_ext_dist_ejes2 = Field()
    dim_ext_trocha_del2 = Field()
    dim_ext_trocha_tra2 = Field()
    dim_ext_diam_giro2 = Field()
    dim_cap_baul_techo2 = Field()

    # especificaciones - frenos
    freno_disco = Field()
    freno_disco_num = Field()
    freno_disco_num_disc_vent = Field()
    freno_ABS = Field()
    freno_servofreno_emergencia = Field()
    freno_aus_bajato = Field()

    # especificaciones - garantia
    g_vehiculo_completo = Field()
    g_vehiculo_completo_duracion = Field()
    g_vehiculo_completo_distancia1 = Field()
    g_vehiculo_completo_distancia2 = Field()

    # especificaciones - llantas
    # TODO: completar con los atributos faltantes

    # especificaciones - motor
    motor_em = Field()
    motor_cc_em = Field()
    motor_litros_em = Field()
    motor_cilindros_em = Field()
    motor_config_em = Field()
    motor_arbol_levas_em = Field()
    motor_valv_cil_em = Field()
    motor_cod_motor_em = Field()

    # especificaciones - pesos
    # especificaciones - segmentacion
    # especificaciones - suspension
    # especificaciones - transmision
    # especificaciones - version
    # TODO: completar con los atributos faltantes

    # DATOS DE CONTACTO
    contact_seller = Field()
    contact_seller_url = Field()
    contact_name = Field()
    contact_number = Field()
    contact_address = Field()
    contact_comuna = Field()
    contact_city = Field()
    contact_region = Field()

    # EQUIPAMIENTO
    eq_air_acon = Field()
    eq_alzavid = Field()
    eq_airbag = Field()
    eq_cierre_cent = Field()
    eq_llantas = Field()
    eq_direccion = Field()
    eq_techo = Field()
    eq_puertas = Field()
    eq_cilindrada = Field()

    #AMOTOR
    idvehiculo_amotor = Field()
    idvehiculo2_amotor = Field()
    patente_amotor = Field()
    IdCategoria_amotor = Field()
    Categoria_amotor = Field()
    Idsucursal_amotor = Field()
    sucursal_amotor = Field()
    Idmarca_amotor = Field()
    Idmodelo_amotor = Field()
    transmision_amotor = Field()
    combustible_amotor = Field()
    direccion_amotor = Field()
    techo_amotor = Field()
    cilindrada_amotor = Field()
    color_amotor = Field()
    segmento_amotor = Field()
    tapiz_amotor = Field()



class ZoogleItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass
